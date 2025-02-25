# Medi_Ai DOCTOR VOICE BOT
This project is an AI-powered medical voice assistant designed to assist in analyzing medical receipts, identify diseases, and suggest remedies, converting speech to text for patients, generating doctor responses using a multimodal language model, and providing voice output. It integrates Groq API, Speech-to-Text (STT), Text-to-Speech (TTS), and a Gradio-based UI to create an interactive and efficient healthcare assistant.

---
## Setting Up `doctor.py`
### 1. Create a Pipenv Virtual Environment
```sh
pipenv shell
```

### 2. Set Up Groq API Key
1. Visit [Groq Cloud](https://groq.com) and create a new API key.
2. Install the Groq library:
   ```sh
   pipenv install groq
   ```
3. Create a `.env` file and add:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

### 3. Convert Image to Required Format
- The system processes images to extract medical details.

### 4. Multimodal LLM Setup
- Model used: `llama-3.2-11b-vision-preview`

---
## Creating `patient_voice.py`
### 1. Set Up Audio Recorder (FFmpeg & PortAudio)
#### **Windows Installation**
- **Install FFmpeg:** Download and install from [FFmpeg Official Site](https://ffmpeg.org/download.html)
- **Install PortAudio:** Download from [PortAudio](http://www.portaudio.com/download.html) and install following provided instructions.

#### **Linux/Mac Installation**
```sh
sudo apt install ffmpeg portaudio19-dev  # Debian/Ubuntu
brew install ffmpeg portaudio  # macOS
```

### 2. Set Up Speech-to-Text (STT) Model
1. Install necessary libraries:
   ```sh
   pipenv install speechrecognition pydub
   ```

---
## Creating `doctor_voice.py`
### 1. Set Up Text-to-Speech (TTS) Model
- **TTS Models Used:**
  - `gtts` (Google Text-to-Speech)
  - `ElevenLabs` (for high-quality voice output)

### 2. Install Required Libraries
```sh
pipenv install gtts elevenlabs
```

### 3. Set Up ElevenLabs API Key
1. Get your API key from [ElevenLabs](https://elevenlabs.io)
2. Add it to `.env` file:
   ```env
   ELEVENLABS_API_KEY=your_api_key_here
   ```

---
## Setting Up the UI (`gradio_app.py`)
### 1. Install Gradio
```sh
pipenv install gradio
```

### 2. Build the User Interface
- The UI allows users to interact with the VoiceBot AI by uploading an image and providing voice input.
- Gradio is used for a simple and effective web interface.

---
## Running the Application
To launch the VoiceBot AI, activate the Pipenv shell and run:
```sh
pipenv shell
python gradio_app.py
```

The application will be available at `http://127.0.0.1:7860`

# **Project Phases and Commands**  

### **1: Run doctor.py**  
```sh
python doctor.py
```

### **2: Run patient_voice.py**  
```sh
python patient_voice.py
```

### **3: Run doctor_voice.py**  
```sh
python doctor_voice.py
```

### **4: Setup UI for the Voice Bot**  
```sh
python gradio_app.py
```


