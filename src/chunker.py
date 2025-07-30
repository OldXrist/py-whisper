import os
from pydub import AudioSegment
from .config import Config
from .utils import logger, ensure_dir


class AudioChunker:
    def __init__(self):
        self.config = Config()


    def get_audio_duration(self, audio_path):
        try:
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # Duration in seconds
        except Exception as e:
            logger.error(f"Error getting audio duration: {str(e)}")
            raise


    def split_audio(self, audio_path):
        try:
            logger.info(f"Checking if {audio_path} needs splitting")
            file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
            if file_size_mb <= self.config.MAX_CHUNK_SIZE_MB:
                logger.info(f"File size {file_size_mb:.2f}MB is under limit, no splitting needed")
                return [audio_path]

            audio = AudioSegment.from_file(audio_path)
            duration_ms = len(audio)
            # Estimate chunk duration to keep under MAX_CHUNK_SIZE_MB
            # Assuming WAV bitrate ~1.4Mbps for 16-bit stereo 44.1kHz
            bitrate_kbps = audio.frame_rate * audio.frame_width * audio.channels * 8 / 1000
            chunk_size_ms = int((self.config.MAX_CHUNK_SIZE_MB * 1024 * 1024 * 8 * 1000) / (bitrate_kbps * 1000))

            chunks = []
            ensure_dir(self.config.OUTPUT_DIR)
            base_name = os.path.basename(audio_path).rsplit(".", 1)[0]

            for i in range(0, duration_ms, chunk_size_ms):
                chunk = audio[i:i + chunk_size_ms]
                chunk_path = os.path.join(
                    self.config.OUTPUT_DIR,
                    f"{base_name}_chunk{i // 1000:03d}.wav"
                )
                chunk.export(chunk_path, format="wav")
                chunks.append(chunk_path)
                logger.info(f"Created chunk: {chunk_path}")

            return chunks
        except Exception as e:
            logger.error(f"Error splitting audio: {str(e)}")
            raise
