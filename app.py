"""
Speech-to-Text ASR Tool
A simple, beginner-friendly Automatic Speech Recognition web application
built with Streamlit and OpenAI Whisper.
"""

import os
import tempfile
from pathlib import Path
from typing import Dict, Optional, Tuple

import streamlit as st

# Supported audio extensions
SUPPORTED_AUDIO_FORMATS = ["wav", "mp3", "m4a", "flac"]

# Common language choices mapping to ISO-639-1 codes (None indicates auto-detection)
LANGUAGE_MAPPING: Dict[str, Optional[str]] = {
    "Auto Detect": None,
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh",
    "Japanese": "ja",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
}


def get_supported_languages() -> Dict[str, Optional[str]]:
    """Return the dictionary of supported languages and their codes."""
    return LANGUAGE_MAPPING


def validate_audio_file(uploaded_file) -> Tuple[bool, str]:
    """
    Validate that an uploaded file exists, is non-empty, and has a supported extension.

    Returns:
        (is_valid, error_message): Tuple indicating success and any error message.
    """
    if uploaded_file is None:
        return False, "No file uploaded. Please select an audio file."

    # Check for empty file
    file_size = getattr(uploaded_file, "size", None)
    if file_size is not None and file_size == 0:
        return False, "The uploaded file is empty. Please choose a valid audio file."

    # Verify file extension
    file_name = getattr(uploaded_file, "name", "")
    extension = file_name.split(".")[-1].lower() if "." in file_name else ""
    if extension not in SUPPORTED_AUDIO_FORMATS:
        allowed = ", ".join([f".{ext}" for ext in SUPPORTED_AUDIO_FORMATS])
        return (
            False,
            f"Unsupported file format '{extension}'. Supported formats are: {allowed}",
        )

    return True, ""


def save_temp_audio(uploaded_file, target_dir: Optional[str] = None) -> str:
    """
    Save the uploaded audio bytes to a temporary file on disk so Whisper/FFmpeg
    can read it from a real file path.
    """
    file_name = getattr(uploaded_file, "name", "temp_audio.wav")
    extension = file_name.split(".")[-1].lower() if "." in file_name else "wav"
    suffix = f".{extension}"

    if target_dir:
        os.makedirs(target_dir, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix, dir=target_dir
    ) as temp_file:
        # Streamlit UploadedFile supports getbuffer() or read()
        if hasattr(uploaded_file, "getbuffer"):
            temp_file.write(uploaded_file.getbuffer())
        else:
            temp_file.write(uploaded_file.read())
        return temp_file.name


@st.cache_resource(show_spinner=False)
def load_whisper_model(model_name: str = "base"):
    """
    Load and cache the OpenAI Whisper model in memory.
    Cached across app reruns so weights are only downloaded/loaded once.
    """
    import whisper

    return whisper.load_model(model_name)


def transcribe_audio(
    model, audio_path: str, language_code: Optional[str] = None
) -> dict:
    """
    Transcribe an audio file using the provided Whisper model.
    Runs with fp16=False to ensure stable execution across CPU and GPU.
    """
    options = {"fp16": False}
    if language_code and language_code != "auto":
        options["language"] = language_code

    return model.transcribe(audio_path, **options)


def format_transcription(result: Optional[dict]) -> str:
    """Extract and format transcribed text cleanly from the Whisper result dictionary."""
    if not result or not isinstance(result, dict):
        return ""
    text = result.get("text", "")
    return text.strip() if isinstance(text, str) else ""


def main():
    st.set_page_config(
        page_title="Speech-to-Text ASR Tool",
        page_icon="🎙️",
        layout="centered",
    )

    st.title("🎙️ Speech-to-Text ASR Tool")
    st.markdown(
        "Convert spoken words in your audio files into text using "
        "OpenAI's open-source **Whisper** speech recognition model."
    )

    # Sidebar settings
    st.sidebar.header("⚙️ Settings")
    model_name = st.sidebar.selectbox(
        "Whisper Model Size",
        options=["tiny", "base", "small"],
        index=1,
        help=(
            "'tiny' is fastest with minimal RAM usage. "
            "'base' balances speed and accuracy (recommended). "
            "'small' provides higher accuracy at the cost of slightly more time."
        ),
    )

    languages = get_supported_languages()
    selected_language_name = st.sidebar.selectbox(
        "Language",
        options=list(languages.keys()),
        index=0,
        help="Select 'Auto Detect' or specify the spoken language.",
    )
    language_code = languages[selected_language_name]

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**Supported Formats:**\n"
        "- `.wav`, `.mp3`, `.m4a`, `.flac`\n\n"
        "**Requirements:**\n"
        "- Python 3.10+\n"
        "- FFmpeg installed on system"
    )

    # Main upload section
    uploaded_file = st.file_uploader(
        "Upload an audio file",
        type=SUPPORTED_AUDIO_FORMATS,
        help="Choose an audio file in WAV, MP3, M4A, or FLAC format.",
    )

    if uploaded_file is not None:
        is_valid, error_msg = validate_audio_file(uploaded_file)
        if not is_valid:
            st.error(f"❌ {error_msg}")
            return

        file_size_kb = uploaded_file.size / 1024
        st.success(f"File uploaded: **{uploaded_file.name}** ({file_size_kb:.1f} KB)")

        # Audio preview
        st.subheader("🔊 Audio Preview")
        st.audio(uploaded_file)

        # Transcribe button
        if st.button("🚀 Transcribe Audio", type="primary"):
            temp_path = None
            try:
                with st.spinner(
                    f"Loading '{model_name}' model and transcribing audio... Please wait."
                ):
                    # Load model (cached)
                    model = load_whisper_model(model_name)

                    # Save uploaded bytes to a temporary file for Whisper/FFmpeg
                    temp_path = save_temp_audio(uploaded_file)

                    # Run transcription
                    result = transcribe_audio(model, temp_path, language_code)

                transcription_text = format_transcription(result)

                if transcription_text:
                    st.subheader("📝 Transcription Result")
                    st.text_area(
                        label="Recognized Text:",
                        value=transcription_text,
                        height=200,
                    )

                    # Show detected language if auto-detect was used
                    detected_lang = result.get("language")
                    if detected_lang:
                        st.caption(f"Detected language code: `{detected_lang}`")

                    # Download button for text file
                    st.download_button(
                        label="💾 Download Transcription (.txt)",
                        data=transcription_text,
                        file_name=f"{Path(uploaded_file.name).stem}_transcription.txt",
                        mime="text/plain",
                    )
                else:
                    st.warning("⚠️ No speech was detected in the audio file.")

            except Exception as e:
                st.error(f"❌ Transcription error: {str(e)}")
                st.info(
                    "💡 Tip: Ensure FFmpeg is installed and accessible in your system PATH."
                )

            finally:
                # Clean up temporary file
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass


if __name__ == "__main__":
    main()
