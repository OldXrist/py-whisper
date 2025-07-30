import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in .env file")
        self.WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-large-v3")
        self.SUPPORTED_AUDIO_FORMATS = set(os.getenv("SUPPORTED_AUDIO_FORMATS", ".wav,.mp3,.m4a").split(","))
        self.SUPPORTED_VIDEO_FORMATS = set(os.getenv("SUPPORTED_VIDEO_FORMATS", ".mp4,.avi,.mov").split(","))
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR", "transcriptions")
        self.LOG_DIR = os.getenv("LOG_DIR", "logs")
        self.LOG_FILE = os.path.join(self.LOG_DIR, os.getenv("LOG_FILE", "transcription.log"))
        self.MAX_CHUNK_SIZE_MB = int(os.getenv("MAX_CHUNK_SIZE_MB", 90))
