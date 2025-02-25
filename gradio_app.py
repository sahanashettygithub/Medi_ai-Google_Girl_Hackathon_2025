import os
import time
import gradio as gr

from doctor import encode_image, analyze_image_with_query
from patient_voice import record_audio, transcribe_with_groq
from doctor_voice import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# Load ElevenLabs API Key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("❌ ELEVENLABS_API_KEY is missing! Set it as an environment variable.")

# System Prompt
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image? Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Do not say 'In the image I see' but say 'With what I see, I think you have ....'
            Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot. 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""


# Function to Process Inputs
def process_inputs(audio_filepath, image_filepath):
    # Speech-to-Text Conversion
    print("🎙️ Converting Speech to Text...")
    try:
        speech_to_text_output = transcribe_with_groq(
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    except Exception as e:
        print(f"❌ Speech-to-Text Error: {e}")
        return "Error in speech-to-text conversion.", "", None

    # Image Analysis
    if image_filepath:
        print("🖼️ Analyzing Image...")
        try:
            doctor_response = analyze_image_with_query(
                query=system_prompt + " " + speech_to_text_output,
                encoded_image=encode_image(image_filepath),
                model="llama-3.2-11b-vision-preview"
            )
        except Exception as e:
            print(f"❌ Image Analysis Error: {e}")
            doctor_response = "Error in analyzing the image."
    else:
        doctor_response = "No image provided for me to analyze."

    # Text-to-Speech Conversion
    print("🔊 Converting Text to Speech...")
    try:
        output_audio_path = "final_doctor_response.mp3"
        text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=output_audio_path)
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        return speech_to_text_output, doctor_response, None

    return speech_to_text_output, doctor_response, output_audio_path


# Create Gradio Interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Output")
    ],
    title="🩺 Doctor Voice Bot",
    description="🎙️ Speak into the microphone and/or upload an image. Get a professional doctor-like response with voice output."
)

# Launch App
iface.launch(debug=True) 