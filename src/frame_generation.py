import torch
import numpy as np
import cv2
import face_recognition
import webrtcvad
from pydub import AudioSegment
from pydub.silence import split_on_silence
from urllib.request import urlopen
import dnnlib
import legacy
import os
import uuid
from cassandra.cluster import Cluster
from PIL import Image
from HighResGenerator import HighResGenerator  # Ensure these imports are correct
from Wav2LipInferencer import Wav2LipInferencer  # Ensure these imports are correct

device = "cuda" if torch.cuda.is_available() else "cpu"
highres_generator = HighResGenerator(input_dim=100, output_channels=3).to(device)
wav2lip_model = Wav2LipInferencer('path_to_wav2lip_model', device=device)  # Initialize the Wav2Lip model

def load_stylegan3_model(model_path):
    print(f'Loading networks from "{model_path}"...')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    with dnnlib.util.open_url(model_path) as f:
        G = legacy.load_network_pkl(f)['G_ema'].to(device)  # subclass of torch.nn.Module
    
    return G

def generate_frame(G, z, truncation_psi=0.5):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    z = torch.from_numpy(z).to(device)
    label = torch.zeros([1, G.c_dim], device=device)
    
    with torch.no_grad():
        img = G(z, label, truncation_psi=truncation_psi, noise_mode='const')
    
    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
    img = Image.fromarray(img[0].cpu().numpy(), 'RGB')
    return img

def generate_coherent_frames(G, output_dir, num_frames=30, truncation_psi=0.5):
    z_start = np.random.randn(1, G.z_dim)
    z_end = np.random.randn(1, G.z_dim)
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i, t in enumerate(np.linspace(0, 1, num_frames)):
        z = (1 - t) * z_start + t * z_end
        frame = generate_frame(G, z, truncation_psi=truncation_psi)
        frame.save(os.path.join(output_dir, f'frame_{i:03d}.png'))

def get_character_profile(character_id):
    """ Retrieve the character profile from ScyllaDB based on character_id. """
    cluster = Cluster(['127.0.0.1'])  # Specify ScyllaDB IPs
    session = cluster.connect('watchai')  # Use your specific keyspace
    try:
        character_uuid = uuid.UUID(character_id)
        query = "SELECT * FROM character_profiles WHERE character_id = %s"
        profile = session.execute(query, [character_uuid]).one()
        return profile
    except ValueError:
        print("Invalid UUID format.")
        return None
    finally:
        session.shutdown()

def identify_faces(frame, known_face_encodings, known_face_names):
    """Identifies faces in a frame."""
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        face_names.append(name)
    return face_locations, face_names

def download_image(url):
    """ Download an image from a URL and return it as an OpenCV image. """
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def add_image_to_frame(frame, image, x_offset=50, y_offset=50):
    """ Add an image to a frame at specified offsets. """
    frame_height, frame_width, _ = frame.shape
    image_height, image_width, _ = image.shape
    end_y = y_offset + image_height
    end_x = x_offset + image_width
    
    if end_y <= frame_height and end_x <= frame_width:
        frame[y_offset:end_y, x_offset:end_x] = image

def get_faces(frame):
    """Detect faces in the frame using DNN."""
    face_model = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000_fp16.caffemodel')
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_model.setInput(blob)
    detections = face_model.forward()
    faces = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:  # threshold
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x2, y2) = box.astype("int")
            faces.append((x, y, x2-x, y2-y))
    return faces

def check_speech_in_audio(audio_path):
    """Analyzes the audio file to detect if there is speech present."""
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1)
    
    chunks = split_on_silence(
        audio,
        min_silence_len=300,
        silence_thresh=-40,
        keep_silence=200
    )

    vad = webrtcvad.Vad()
    vad.set_mode(3)

    for chunk in chunks:
        if len(chunk) < 10:
            continue
        
        frame = bytes(chunk.raw_data)
        if vad.is_speech(frame, audio.frame_rate):
            return True

    return False

def recognize_faces(frame, known_faces):
    """Identify faces in the frame given known face encodings."""
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces["encodings"], face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_faces["names"][first_match_index]
        face_names.append(name)
    return face_locations, face_names    

def apply_wav2lip(face_img, audio_path):
    """ Applies the Wav2Lip model to synchronize lips in the face image based on the audio. """
    return wav2lip_model.apply_lip_sync(face_img, audio_path)
