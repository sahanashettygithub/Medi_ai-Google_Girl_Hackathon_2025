import os
import subprocess
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment  # Converts MP3 to WAV (for Windows)

# Load API Key (ensure it's set in your environment variables)
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def convert_mp3_to_wav(mp3_filepath, wav_filepath):
    """Converts MP3 to WAV for Windows compatibility."""
    try:
        audio = AudioSegment.from_mp3(mp3_filepath)
        audio.export(wav_filepath, format="wav")
        return wav_filepath
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        return None

def play_audio(file_path):
    """Plays audio based on the OS."""
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(["afplay", file_path])
        elif os_name == "Windows":  # Windows requires WAV
            wav_path = file_path.replace(".mp3", ".wav")
            wav_file = convert_mp3_to_wav(file_path, wav_path)
            if wav_file:
                subprocess.run(["powershell", "-c", f'(New-Object Media.SoundPlayer "{wav_file}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(["mpg123", file_path])  
        else:
            print("Unsupported OS")
    except Exception as e:
        print(f"Error playing audio: {e}")

def text_to_speech_with_gtts(input_text, output_filepath):
    """Converts text to speech using gTTS and plays it."""
    try:
        tts = gTTS(text=input_text, lang="en", slow=False)
        tts.save(output_filepath)
        print(f"gTTS audio saved: {output_filepath}")
        play_audio(output_filepath)
    except Exception as e:
        print(f"Error in gTTS: {e}")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """Converts text to speech using ElevenLabs and plays it."""
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio_generator = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        with open(output_filepath, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)

        print(f"ElevenLabs audio saved: {output_filepath}")
        play_audio(output_filepath)
    except Exception as e:
        print(f"Error in ElevenLabs TTS: {e}")


input_text = "Hi, this is Sahana. Testing autoplay!"
gtts_output = "gtts_output.mp3"
#text_to_speech_with_gtts(input_text, gtts_output)

elevenlabs_output = "elevenlabs_output.mp3"
#text_to_speech_with_elevenlabs(input_text, elevenlabs_output)  
