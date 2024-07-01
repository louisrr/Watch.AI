from moviepy.editor import ImageSequenceClip, VideoFileClip, AudioFileClip, CompositeVideoClip
from cassandra.cluster import Cluster
import speech_recognition as sr
from pyAudioAnalysis import audioSegmentation as aS

def speaker_diarization(audio_path, num_speakers):
    """Returns intervals of audio for each speaker."""
    [flags, classes, acc, _] = aS.speaker_diarization(audio_path, num_speakers, mid_window=1.0, mid_step=0.1, short_window=0.05, lda_dim=0, plot_res=False)
    return flags, classes

def transcribe_audio(audio_path):
    """Transcribes audio to text with timestamps."""
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        transcript = r.recognize_google(audio, show_all=True)  # Using Google Web Speech API
        return transcript
    except sr.UnknownValueError:
        return "Audio could not be understood"
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service"    

def add_audio_to_video(video_file, audio_file, final_output="final_video.mp4"):
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(final_output, codec="libx264")

def get_voice_profile(profile_name):
    """ Retrieve the voice profile from ScyllaDB. """
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('your_keyspace')
    result = session.execute("SELECT * FROM voice_profiles WHERE profile_name = %s", [profile_name])
    return result.one()

def synthesize_speech(text, profile_name):
    """ Synthesize speech using a specific voice profile. """
    profile_data = get_voice_profile(profile_name)
    if profile_data:
        # Assume CoquiTTS has a function to synthesize voice
        CoquiTTS.synthesize(text, profile_data['model_path'])
    else:
        print("Profile not found.")

def compile_video(frames, fps=24, output_file="output_video.mp4", audio_path=None):
    """
    Compiles video from frames and synchronizes with an audio file.

    Args:
    frames (list): A list of image frames (as np.arrays or file paths).
    fps (int): Frames per second of the output video.
    output_file (str): Filename for the output video.
    audio_path (str, optional): Path to the audio file to synchronize with the video.

    """
    # Create a video clip from image frames
    clip = ImageSequenceClip(frames, fps=fps)
    
    if audio_path:
        # If an audio path is provided, synchronize it with the video
        audio_clip = AudioFileClip(audio_path)
        # Adjust audio clip to the length of the video clip if necessary
        if audio_clip.duration > clip.duration:
            audio_clip = audio_clip.subclip(0, clip.duration)
        # Set the audio of the video clip
        clip = clip.set_audio(audio_clip)
    
    # Write the composite video file with audio
    clip.write_videofile(output_file, codec="libx264")
