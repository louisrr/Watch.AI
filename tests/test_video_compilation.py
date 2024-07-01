import pytest
from unittest.mock import patch, MagicMock
from my_script import speaker_diarization, transcribe_audio, add_audio_to_video, get_voice_profile, synthesize_speech, compile_video  # Replace with the actual name of your script

@pytest.fixture
def mock_dependencies():
    with patch('my_script.aS.speaker_diarization') as mock_speaker_diarization, \
         patch('my_script.sr.Recognizer') as mock_recognizer, \
         patch('my_script.VideoFileClip') as mock_video_clip, \
         patch('my_script.AudioFileClip') as mock_audio_clip, \
         patch('my_script.Cluster') as mock_cluster, \
         patch('my_script.CoquiTTS') as mock_coqui_tts, \
         patch('my_script.ImageSequenceClip') as mock_image_sequence_clip:
        
        yield {
            'mock_speaker_diarization': mock_speaker_diarization,
            'mock_recognizer': mock_recognizer,
            'mock_video_clip': mock_video_clip,
            'mock_audio_clip': mock_audio_clip,
            'mock_cluster': mock_cluster,
            'mock_coqui_tts': mock_coqui_tts,
            'mock_image_sequence_clip': mock_image_sequence_clip
        }

def test_speaker_diarization(mock_dependencies):
    mock_dependencies['mock_speaker_diarization'].return_value = ([0, 1, 0, 1], ['speaker1', 'speaker2'])
    flags, classes = speaker_diarization("audio_path", 2)
    assert flags == [0, 1, 0, 1]
    assert classes == ['speaker1', 'speaker2']
    mock_dependencies['mock_speaker_diarization'].assert_called_once_with("audio_path", 2, mid_window=1.0, mid_step=0.1, short_window=0.05, lda_dim=0, plot_res=False)

def test_transcribe_audio(mock_dependencies):
    mock_recognizer_instance = mock_dependencies['mock_recognizer'].return_value
    mock_recognizer_instance.recognize_google.return_value = {'transcript': 'test transcription'}
    transcript = transcribe_audio("audio_path")
    assert transcript == {'transcript': 'test transcription'}

def test_add_audio_to_video(mock_dependencies):
    mock_video_clip_instance = mock_dependencies['mock_video_clip'].return_value
    mock_audio_clip_instance = mock_dependencies['mock_audio_clip'].return_value
    add_audio_to_video("video_file.mp4", "audio_file.mp3", "final_output.mp4")
    mock_video_clip_instance.set_audio.assert_called_once_with(mock_audio_clip_instance)
    mock_video_clip_instance.write_videofile.assert_called_once_with("final_output.mp4", codec="libx264")

def test_get_voice_profile(mock_dependencies):
    mock_session = mock_dependencies['mock_cluster'].return_value.connect.return_value
    mock_session.execute.return_value.one.return_value = {'profile_name': 'test_profile', 'model_path': 'path/to/model'}
    profile = get_voice_profile("test_profile")
    assert profile == {'profile_name': 'test_profile', 'model_path': 'path/to/model'}
    mock_session.execute.assert_called_once_with("SELECT * FROM voice_profiles WHERE profile_name = %s", ["test_profile"])

def test_synthesize_speech(mock_dependencies):
    mock_dependencies['mock_cluster'].return_value.connect.return_value.execute.return_value.one.return_value = {'profile_name': 'test_profile', 'model_path': 'path/to/model'}
    synthesize_speech("Hello world", "test_profile")
    mock_dependencies['mock_coqui_tts'].synthesize.assert_called_once_with("Hello world", 'path/to/model')

def test_compile_video(mock_dependencies):
    mock_image_sequence_clip_instance = mock_dependencies['mock_image_sequence_clip'].return_value
    compile_video(["frame1.png", "frame2.png"], fps=24, output_file="output_video.mp4", audio_path="audio_file.mp3")
    mock_dependencies['mock_image_sequence_clip'].assert_called_once_with(["frame1.png", "frame2.png"], fps=24)
    mock_image_sequence_clip_instance.set_audio.assert_called_once()
    mock_image_sequence_clip_instance.write_videofile.assert_called_once_with("output_video.mp4", codec="libx264")

