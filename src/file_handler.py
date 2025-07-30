import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from .config import Config
from .utils import logger


class FileHandler:
    def __init__(self):
        config = Config()
        self.supported_formats = (
                config.SUPPORTED_AUDIO_FORMATS | config.SUPPORTED_VIDEO_FORMATS
        )


    def validate_file(self, file_path):
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self.supported_formats:
            logger.error(f"Unsupported file format: {ext}")
            raise ValueError(f"Unsupported file format: {ext}")

        return True


    def extract_audio_from_video(self, video_path, output_audio_path):
        try:
            logger.info(f"Extracting audio from video: {video_path}")
            video = VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(output_audio_path)
            audio.close()
            video.close()
            logger.info(f"Audio extracted to: {output_audio_path}")
            return output_audio_path
        except Exception as e:
            logger.error(f"Error extracting audio: {str(e)}")
            raise


    def convert_to_wav(self, audio_path):
        try:
            _, ext = os.path.splitext(audio_path)
            if ext.lower() != ".wav":
                logger.info(f"Converting {audio_path} to WAV")
                audio = AudioSegment.from_file(audio_path)
                wav_path = audio_path.rsplit(".", 1)[0] + ".wav"
                audio.export(wav_path, format="wav")
                return wav_path
            return audio_path
        except Exception as e:
            logger.error(f"Error converting to WAV: {str(e)}")
            raise
