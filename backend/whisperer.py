import torch
import logging
from pathlib import Path
from pytube import YouTube, exceptions as pytube_exceptions

import whisper

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load the desired model (assuming Whisper is installed and set up)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("medium.en").to(DEVICE)
#print(type(model))

def to_snake_case(name):
    name = name.lower().replace(" ", "_").replace(":", "_")
    return name.replace("/", "-").replace("__", "_")


def download_youtube_audio(url, out_dir="."):
    """Download the audio from a YouTube video."""
    try:
        yt = YouTube(url)
    except pytube_exceptions.PytubeError as e:
        logging.error(f"Failed to download video: {e}")
        return None
    
    # Ensure the directory exists
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate the sanitized filename
    file_name = Path(out_dir, to_snake_case(yt.title)).with_suffix(".mp4")

    # Log the directory and filename for debugging
    logging.info(f"Directory: {out_dir}, Filename: {file_name}")
    
    yt = (yt.streams
        .filter(only_audio=True, file_extension="mp4")
        .order_by("abr")
        .desc())
    return yt.first().download(filename=file_name)


def transcribe_audio_to_text(model, audio_file):
    """Transcribe an audio file to text using Whisper."""
    try:
        result = model.transcribe(audio_file, verbose=False, language="en")
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {e}")
        return None
    
    return result["text"]

def youtube_to_transcription(youtube_url):
    """Wrapper function: From a YouTube URL to transcribed text."""
    # Step 1: Download audio from YouTube
    audio_file = download_youtube_audio(youtube_url)
    if audio_file is None: 
        return None
    
    # Step 2: Transcribe the audio to text
    transcribed_text = transcribe_audio_to_text(model, audio_file)
    if transcribed_text is None:
        return None
    
    return transcribed_text

# Example usage:
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=5iN2SvFyRjY"
    result = youtube_to_transcription(youtube_url)
    if result:
        print(result)
    else:
        logging.error("Transcription failed.")
