🎙️ Speech-to-Text ASR Tool

A simple, beginner-friendly Automatic Speech Recognition (ASR) web application built using Python, and Streamlit.

This application allows users to upload an audio file (e.g., speech or voice recording) and convert spoken words into clean text using OpenAI's state-of-the-art open-source Whisper model. It provides an intuitive web interface, audio preview playback, language selection or auto-detection, and one-click transcription download.

 Features

- Multi-Format Audio Upload**: Supports popular audio formats: `.wav`, `.mp3`, `.m4a`, and `.flac`.
- Open-Source Whisper ASR**: Uses OpenAI's Whisper model (`tiny`, `base`, or `small`) running locally on CPU or GPU.
- Language Detection & Selection**: Automatically detects spoken languages or allows users to choose from a list of languages.
- Model Caching: Utilizes Streamlit's `@st.cache_resource` to keep model weights loaded in memory, avoiding redundant downloads and reloads.
- Audio Playback Preview**: Built-in audio player to listen to recordings before transcribing.
- One-Click Export**: Save the generated transcript directly to a `.txt` file with a download button.
- Error Handling & Validation**: Gracefully checks for empty files, unsupported extensions, and transcription errors.
- Lightweight & Beginner-Friendly**: Clean, modular codebase suitable for university students and introductory AI projects.


 🛠️ Technologies Used

- Python 3.10+: Core programming language.
- OpenAI Whisper: Open-source neural network for speech recognition.
- Streamlit: Web framework for building interactive data and AI apps in pure Python.
- FFmpeg: Multimedia processing framework required by Whisper to read and decode audio files.
-pytest: Framework for running automated unit tests.
- Git & GitHub: Version control and project repository hosting.


Prerequisites

Before running this project, ensure you have:
1. Python 3.10 or higher installed ([Download Python](https://www.python.org/downloads/)).
2. FFmpeg installed and added to your system's `PATH`.

⚙️ FFmpeg Setup for Windows

OpenAI Whisper depends on FFmpeg to decode audio files. Follow any of the options below to install it on Windows:

Option 1: Using Windows Package Manager (`winget`) — Recommended
Open PowerShell or Command Prompt and run:
```powershell
winget install Gyan.FFmpeg
```
After installation completes, **close and reopen** your terminal so the updated `PATH` takes effect.

Option 2: Using Chocolatey
If you use [Chocolatey](https://chocolatey.org/):
```powershell
choco install ffmpeg
```

Option 3: Using Scoop
If you use [Scoop](https://scoop.sh/):
```powershell
scoop install ffmpeg
```

Option 4: Manual Installation
1. Download the latest `ffmpeg-release-essentials.zip` from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/).
2. Extract the archive (e.g., to `C:\ffmpeg`).
3. Add the `C:\ffmpeg\bin` folder to your system **Environment Variables** (`PATH`):
   - Press `Win + S`, type `Environment Variables`, and select **Edit the system environment variables**.
   - Click **Environment Variables...**
   - Under *System variables*, select `Path` and click **Edit...**
   - Click **New** and paste `C:\ffmpeg\bin`.
   - Click **OK** to save and close all dialogs
 Verify FFmpeg Installation
Open a new terminal window and run:
```powershell
ffmpeg -version
```
If you see version details, FFmpeg is correctly installed and ready.


📦 Installation & Setup Instructions

Follow these steps to set up and run the application on your computer:

Step 1: Clone or Navigate to the Project
```bash
git clone https://github.com/<your-username>/asr-speech-to-text.git
cd asr-speech-to-text
```

 Step 2: Create a Python Virtual Environment
Creating a virtual environment ensures project dependencies do not interfere with other Python software on your system:
```powershell
 Windows PowerShell
python -m venv .venv
```
 Step 3: Activate the Virtual Environment
```powershell
 Windows PowerShell
.venv\Scripts\Activate.ps1
```
(If you see an execution policy error in PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` first).

On Command Prompt (`cmd.exe`):
```cmd
.venv\Scripts\activate.bat
```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

Note on PyTorch:** If you have an NVIDIA GPU with CUDA and want accelerated GPU inference, you can install the CUDA-enabled build of PyTorch from [pytorch.org](https://pytorch.org/). By default, standard CPU execution will work out-of-the-box.

---

 ▶️ Running the Application

Once dependencies are installed and the virtual environment is activated, launch the Streamlit app:

```powershell
streamlit run app.py
```

The application will start, and your default web browser will automatically open:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

How to Use the App:
1. Select the **Whisper Model Size** in the sidebar (Default: `base`).
2. Choose a **Language** or keep `Auto Detect`.
3. Upload an audio file (`.wav`, `.mp3`, `.m4a`, or `.flac`).
4. Listen to the preview using the audio player.
5. Click **🚀 Transcribe Audio**.
6. View the recognized text in the transcription box and click **💾 Download Transcription (.txt)** to save it.


 🧪 Running Unit Tests

The test suite in `tests/test_app.py` checks input validation, helper routines, language mappings, and error-handling without needing to transcribe real audio or download heavy model weights.

To run the automated tests:
```powershell
pytest -v
```

Expected output:
```
============================= test session starts =============================
collected 13 items

tests/test_app.py::TestAudioValidation::test_valid_audio_extensions[wav] PASSED
tests/test_app.py::TestAudioValidation::test_valid_audio_extensions[mp3] PASSED
tests/test_app.py::TestAudioValidation::test_valid_audio_extensions[m4a] PASSED
tests/test_app.py::TestAudioValidation::test_valid_audio_extensions[flac] PASSED
tests/test_app.py::TestAudioValidation::test_uppercase_audio_extension PASSED
tests/test_app.py::TestAudioValidation::test_none_file PASSED
tests/test_app.py::TestAudioValidation::test_empty_file PASSED
tests/test_app.py::TestAudioValidation::test_unsupported_extensions[document.txt] PASSED
tests/test_app.py::TestAudioValidation::test_unsupported_extensions[video.mp4] PASSED
tests/test_app.py::TestAudioValidation::test_unsupported_extensions[script.py] PASSED
tests/test_app.py::TestAudioValidation::test_unsupported_extensions[audio_no_ext] PASSED
tests/test_app.py::TestLanguageMapping::test_supported_languages_dict PASSED
tests/test_app.py::TestFormatTranscription::test_valid_transcription_result PASSED
tests/test_app.py::TestFormatTranscription::test_empty_or_none_result PASSED
tests/test_app.py::TestFormatTranscription::test_non_dict_result PASSED
tests/test_app.py::TestSaveTempAudio::test_save_and_cleanup PASSED
tests/test_app.py::TestTranscribeAudio::test_transcribe_auto_detect PASSED
tests/test_app.py::TestTranscribeAudio::test_transcribe_specific_language PASSED
tests/test_app.py::TestTranscribeAudio::test_transcribe_handles_exception PASSED
============================== 19 passed in ... ==============================
```

 📁 Project Structure

```
asr-speech-to-text/
├── app.py              # Main Streamlit web application and ASR logic
├── requirements.txt    # Python dependencies (Streamlit, Whisper, pytest)
├── README.md           # Documentation, setup guide, and user instructions
├── .gitignore          # Git exclusion rules (virtual environments, caches, audio)
└── tests/
    └── test_app.py     # Automated unit tests for application logic & validation
```


🎵 Supported Formats & Model Limitations

 Supported Audio Formats
- **WAV** (`.wav`): Uncompressed audio; fast processing and high fidelity.
- **MP3** (`.mp3`): Common compressed audio format.
- **M4A** (`.m4a`): Common format on Apple/mobile devices.
- **FLAC** (`.flac`): Lossless compressed audio format.

 Whisper Model Overview
| Model | Parameters | Required VRAM / RAM | Relative Speed | Typical Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `tiny` | 39 M | ~1 GB | ~32x | Ultra-fast, minimal memory, clear speech |
| `base` | 74 M | ~1 GB | ~16x | **Recommended default**, great balance |
| `small` | 244 M | ~2 GB | ~6x | Better punctuation & non-English accuracy |

Limitations
- Processing Time: On CPU-only machines, transcribing longer audio files (>5 minutes) may take some time depending on your processor.
- Background Noise: Very noisy environments, heavy accents, or overlapping speakers may reduce transcription accuracy.
- FFmpeg Required: Audio decoding relies on system FFmpeg. If FFmpeg is missing, Whisper will throw an error when loading audio files.


 
