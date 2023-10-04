from langchain.tools import BaseTool
from typing import Union, Optional
from whisperer import youtube_to_transcription, model 
class YouTubeTranscriptionTool(BaseTool):
    name = "YouTube Transcription"
    description = "This tool transcribes YouTube videos into text using the Whisper ASR model."

    def __init__(self):
        # Initialize Whisper model and other resources here if needed
        self.model = model  

    def _run(self, youtube_url: str) -> Optional[str]:
        transcribed_text = youtube_to_transcription(youtube_url)
        if transcribed_text:
            return transcribed_text
        else:
            return "Transcription failed."

    def _arun(self, youtube_url: str) -> None:
        raise NotImplementedError("This tool does not support async")
