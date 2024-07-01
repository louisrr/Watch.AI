import pytest
import torch
import numpy as np
from unittest.mock import patch, MagicMock
from urllib.request import urlopen
from data_collection import (
    get_character_profile,
    identify_faces,
    download_image,
    add_image_to_frame,
    get_faces,
    check_speech_in_audio,
    recognize_faces,
    apply_wav2lip,
    generate_frames
)

@pytest.fixture
def mock_torch():
    with patch('data_collection.torch') as mock_torch:
        mock_torch.cuda.is_available.return_value = True
        mock_torch.randn.return_value = MagicMock()
        yield mock_torch

@pytest.fixture
def mock_cassandra():
    with patch('data_collection.Cluster') as MockCluster:
        mock_session = MagicMock()
        MockCluster.return_value.connect.return_value = mock_session
        yield mock_session

@pytest.fixture
def mock_cv2():
    with patch('data_collection.cv2') as mock_cv2:
        yield mock_cv2

@pytest.fixture
def mock_face_recognition():
    with patch('data_collection.face_recognition') as mock_face_recognition:
        yield mock_face_recognition

@pytest.fixture
def mock_pydub():
    with patch('data_collection.AudioSegment') as mock_audio_segment:
        with patch('data_collection.split_on_silence') as mock_split_on_silence:
            yield mock_audio_segment, mock_split_on_silence

@pytest.fixture
def mock_webrtcvad():
    with patch('data_collection.webrtcvad') as mock_webrtcvad:
        yield mock_webrtcvad

@pytest.fixture
def mock_urlopen():
    with patch('data_collection.urlopen') as mock_urlopen:
        yield mock_urlopen

@pytest.fixture
def mock_highres_generator():
    with patch('data_collection.HighResGenerator') as MockHighResGenerator:
        mock_instance = MockHighResGenerator.return_value
        mock_instance.to.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_wav2lip_inferencer():
    with patch('data_collection.Wav2LipInferencer') as MockWav2LipInferencer:
        mock_instance = MockWav2LipInferencer.return_value
        yield mock_instance

def test_get_character_profile(mock_cassandra):
    mock_cassandra.execute.return_value.one.return_value = {"character_id": uuid.uuid4()}
    character_id = "12345678-1234-1234-1234-123456789012"
    profile = get_character_profile(character_id)
    assert profile is not None
    mock_cassandra.execute.assert_called_once()

def test_identify_faces(mock_face_recognition):
    frame = np.zeros((100, 100, 3))
    known_face_encodings = [np.zeros((128,))]
    known_face_names = ["Test"]
    mock_face_recognition.face_locations.return_value = [(0, 0, 10, 10)]
    mock_face_recognition.face_encodings.return_value = [np.zeros((128,))]
    mock_face_recognition.compare_faces.return_value = [True]

    locations, names = identify_faces(frame, known_face_encodings, known_face_names)
    assert names == ["Test"]
    mock_face_recognition.face_locations.assert_called_once_with(frame)
    mock_face_recognition.face_encodings.assert_called_once_with(frame, [(0, 0, 10, 10)])
    mock_face_recognition.compare_faces.assert_called_once()

def test_download_image(mock_urlopen):
    url = "http://example.com/image.jpg"
    mock_response = MagicMock()
    mock_response.read.return_value = np.zeros((100,), dtype=np.uint8).tobytes()
    mock_urlopen.return_value = mock_response

    image = download_image(url)
    assert image is not None
    mock_urlopen.assert_called_once_with(url)

def test_add_image_to_frame(mock_cv2):
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    image = np.ones((10, 10, 3), dtype=np.uint8)
    add_image_to_frame(frame, image)
    assert np.array_equal(frame[50:60, 50:60], image)

def test_get_faces(mock_cv2):
    frame = np.zeros((300, 300, 3), dtype=np.uint8)
    mock_cv2.dnn.readNetFromCaffe.return_value = MagicMock()
    mock_cv2.dnn.blobFromImage.return_value = np.zeros((1, 3, 300, 300))
    mock_cv2.dnn.readNetFromCaffe.return_value.forward.return_value = np.zeros((1, 1, 1, 7))

    faces = get_faces(frame)
    assert faces == []

def test_check_speech_in_audio(mock_pydub, mock_webrtcvad):
    mock_audio_segment, mock_split_on_silence = mock_pydub
    mock_audio = MagicMock()
    mock_audio_segment.from_file.return_value = mock_audio
    mock_split_on_silence.return_value = [MagicMock()]
    mock_webrtcvad.Vad.return_value.is_speech.return_value = True

    result = check_speech_in_audio("path/to/audio.mp3")
    assert result is True

def test_recognize_faces(mock_face_recognition):
    frame = np.zeros((100, 100, 3))
    known_faces = {"encodings": [np.zeros((128,))], "names": ["Test"]}
    mock_face_recognition.face_locations.return_value = [(0, 0, 10, 10)]
    mock_face_recognition.face_encodings.return_value = [np.zeros((128,))]
    mock_face_recognition.compare_faces.return_value = [True]

    locations, names = recognize_faces(frame, known_faces)
    assert names == ["Test"]

def test_apply_wav2lip(mock_wav2lip_inferencer):
    face_img = np.zeros((100, 100, 3), dtype=np.uint8)
    audio_path = "path/to/audio.mp3"
    mock_wav2lip_inferencer.apply_lip_sync.return_value = face_img

    result = apply_wav2lip(face_img, audio_path)
    assert result is not None
    mock_wav2lip_inferencer.apply_lip_sync.assert_called_once_with(face_img, audio_path)

def test_generate_frames(mock_torch, mock_highres_generator, mock_wav2lip_inferencer):
    frame_specs = [{}]  # Simplified for test
    audio_path = "path/to/audio.mp3"
    known_faces = {"encodings": [np.zeros((128,))], "names": ["Test"]}
    
    mock_torch.randn.return_value = torch.zeros((1, 100))
    mock_highres_generator.return_value.cpu.return_value.detach.return_value.numpy.return_value = np.zeros((3, 256, 256))

    frames = generate_frames(frame_specs, audio_path, known_faces)
    assert len(frames) == 1
