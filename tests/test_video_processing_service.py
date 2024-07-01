# test_voice_profile.py
import pytest
from unittest.mock import patch, MagicMock
from my_script import extract_audio, check_voice_presence, create_voice_profile, save_profile_to_db, process_video  # Replace with the actual name of your script

@pytest.fixture
def mock_dependencies():
    with patch('my_script.mp.VideoFileClip') as mock_video_file_clip, \
         patch('my_script.Cluster') as mock_cluster, \
         patch('my_script.CoquiTTS') as mock_coqui_tts, \
         patch('my_script.datetime') as mock_datetime, \
         patch('my_script.uuid') as mock_uuid:
        
        mock_audio_clip = MagicMock()
        mock_video_file_clip.return_value.audio = mock_audio_clip
        mock_cluster_instance = mock_cluster.return_value
        mock_session = mock_cluster_instance.connect.return_value
        mock_datetime.datetime.now.return_value.strftime.return_value = "20230101120000"
        mock_uuid.uuid4.return_value = "test-uuid"
        
        yield {
            'mock_video_file_clip': mock_video_file_clip,
            'mock_cluster': mock_cluster,
            'mock_coqui_tts': mock_coqui_tts,
            'mock_datetime': mock_datetime,
            'mock_uuid': mock_uuid,
            'mock_audio_clip': mock_audio_clip,
            'mock_session': mock_session
        }

def test_extract_audio(mock_dependencies):
    audio_path = extract_audio("path/to/video.mp4")
    assert audio_path == "AUDIO20230101120000.mp3"
    mock_dependencies['mock_video_file_clip'].assert_called_once_with("path/to/video.mp4")
    mock_dependencies['mock_audio_clip'].write_audiofile.assert_called_once_with("AUDIO20230101120000.mp3")

def test_check_voice_presence(mock_dependencies):
    result = check_voice_presence("path/to/audio.mp3")
    assert result is True

def test_create_voice_profile(mock_dependencies):
    profile_data = create_voice_profile("path/to/audio.mp3")
    assert profile_data == {"profile_id": "test-uuid", "model_path": "path/to/model"}

def test_save_profile_to_db(mock_dependencies):
    save_profile_to_db("user123", "UniqueVoiceProfileName", {"profile_id": "test-uuid", "model_path": "path/to/model"})
    mock_dependencies['mock_session'].execute.assert_called_once_with(
        """
        INSERT INTO voice_profiles (user_id, profile_name, profile_id, model_path, created_at)
        VALUES (%s, %s, %s, %s, toTimestamp(now()))
        """,
        ("user123", "UniqueVoiceProfileName", "test-uuid", "path/to/model")
    )

def test_process_video(mock_dependencies):
    with patch('my_script.extract_audio', return_value="path/to/audio.mp3") as mock_extract_audio, \
         patch('my_script.check_voice_presence', return_value=True) as mock_check_voice_presence, \
         patch('my_script.create_voice_profile', return_value={"profile_id": "test-uuid", "model_path": "path/to/model"}) as mock_create_voice_profile, \
         patch('my_script.save_profile_to_db') as mock_save_profile_to_db:
        
        process_video("path/to/video.mp4", "user123", "UniqueVoiceProfileName")
        
        mock_extract_audio.assert_called_once_with("path/to/video.mp4")
        mock_check_voice_presence.assert_called_once_with("path/to/audio.mp3")
        mock_create_voice_profile.assert_called_once_with("path/to/audio.mp3")
        mock_save_profile_to_db.assert_called_once_with("user123", "UniqueVoiceProfileName", {"profile_id": "test-uuid", "model_path": "path/to/model"})

