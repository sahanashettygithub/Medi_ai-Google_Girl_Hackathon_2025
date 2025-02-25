import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq

# Manually set FFmpeg binary path
FFMPEG_PATH = r"C:\ffmpeg\ffmpeg.exe"
AudioSegment.converter = FFMPEG_PATH
os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=10, phrase_time_limit=None):
    """
    Records audio from the microphone and saves it as an MP3 file.

    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Maximum time to wait for a phrase to start (in seconds).
        phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()

    try:
        # Check if PyAudio is available
        if not sr.Microphone.list_microphone_names():
            logging.error("No microphone found. Ensure PyAudio is installed.")
            return

        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")
    
    except sr.WaitTimeoutError:
        logging.error("No speech detected within the timeout period.")
    except sr.RequestError:
        logging.error("Could not request results from the speech recognition service.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def transcribe_with_groq(stt_model, audio_filepath):
    """
    Transcribes an audio file using Groq's Whisper model.

    Args:
        stt_model (str): The speech-to-text model name.
        audio_filepath (str): Path to the audio file.
    
    Returns:
        str: Transcribed text from the audio file.
    """
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    if not GROQ_API_KEY:
        logging.error("GROQ API key not found. Please set the GROQ_API_KEY environment variable.")
        return None
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"Error in transcription: {e}")
        return None

if __name__ == "__main__":
    audio_filepath = "voice_test_for_patient.mp3"
    record_audio(audio_filepath)
    transcribed_text = transcribe_with_groq("whisper-large-v3", audio_filepath)
    if transcribed_text:
        logging.info(f"Transcription: {transcribed_text}")
