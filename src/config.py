import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        self.WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")
        self.SUPPORTED_AUDIO_FORMATS = set(os.getenv("SUPPORTED_AUDIO_FORMATS", ".wav,.mp3,.m4a").split(","))
        self.SUPPORTED_VIDEO_FORMATS = set(os.getenv("SUPPORTED_VIDEO_FORMATS", ".mp4,.avi,.mov").split(","))
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR", "transcriptions")
        self.LOG_DIR = os.getenv("LOG_DIR", "logs")
        self.LOG_FILE = os.path.join(self.LOG_DIR, os.getenv("LOG_FILE", "transcription.log"))
