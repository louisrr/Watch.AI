import torch
import numpy as np
import cv2
import uuid
from urllib.request import urlopen
from cassandra.cluster import Cluster
from highres_generator import HighResGenerator
from wav2lip_infer import Wav2LipInferencer  # This would be a wrapper you create for Wav2Lip
from pydub import AudioSegment
from pydub.silence import split_on_silence
import webrtcvad
import face_recognition

device = "cuda" if torch.cuda.is_available() else "cpu"
highres_generator = HighResGenerator(input_dim=100, output_channels=3).to(device)
wav2lip_model = Wav2LipInferencer('path_to_wav2lip_model', device=device)  # Initialize the Wav2Lip model

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
    """
    Analyzes the audio file to detect if there is speech present.
    
    Args:
    audio_path (str): Path to the audio file.

    Returns:
    bool: True if speech is detected, False otherwise.
    """
    # Load audio file
    audio = AudioSegment.from_file(audio_path)
    # Assuming the file is stereo, we can convert it to mono
    audio = audio.set_channels(1)
    
    # Split the audio on the basis of silence
    chunks = split_on_silence(
        audio,
        # Use a threshold quieter than -16 dBFS (or adjust to your specific case)
        min_silence_len=300,
        silence_thresh=-40,
        # Keep 200 ms of leading/trailing silence
        keep_silence=200
    )

    vad = webrtcvad.Vad()
    # Set mode (0=normal, 1=low_bitrate, 2=aggressive, 3=very aggressive)
    vad.set_mode(3)

    for chunk in chunks:
        # We need to check if the chunk is longer than 10 ms
        if len(chunk) < 10:
            continue
        
        # Convert pydub audio chunk to bytes
        frame = bytes(chunk.raw_data)
        # Check if current frame has voiced speech
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

def generate_frames(frame_specs, audio_path, known_faces):
    """Generates frames with lip-sync applied to identified faces based on audio analysis."""
    speech_detected = check_speech_in_audio(audio_path)
    transcripts = transcribe_audio(audio_path) if speech_detected else {}

    for spec in frame_specs:
        z = torch.randn(1, 100).to(device)
        frame = highres_generator(z).cpu().detach().numpy()[0].transpose(1, 2, 0)
        frame = (frame * 255).astype(np.uint8)
        
        if speech_detected:
            face_locations, face_names = identify_faces(frame, known_faces)
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if name in transcripts:
                    # Extract the specific audio segment for this speaker
                    segment_audio_path = get_audio_segment_for_speaker(audio_path, transcripts, name)
                    synced_face = apply_wav2lip(frame[top:bottom, left:right], segment_audio_path)
                    frame[top:bottom, left:right] = synced_face
        
        frames.append(frame)
    return frames