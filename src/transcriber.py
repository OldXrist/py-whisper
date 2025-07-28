from openai import OpenAI
from config import Config
from utils import logger, ensure_dir
import os


class Transcriber:
    def __init__(self):
        config = Config()
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.WHISPER_MODEL
        logger.info(f"OpenAI Whisper API model '{self.model}' initialized")

    def transcribe(self, audio_path, output_format="txt"):
        try:
            config = Config()
            logger.info(f"Starting transcription of {audio_path}")
            with open(audio_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format=output_format
                )

            # For txt format, transcription is a string; for srt, it's already formatted
            if output_format == "txt":
                transcription_text = transcription.text
            else:  # srt
                transcription_text = transcription

            ensure_dir(config.OUTPUT_DIR)
            output_file = os.path.join(
                config.OUTPUT_DIR,
                f"{os.path.basename(audio_path).rsplit('.', 1)[0]}.{output_format}"
            )

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcription_text)

            logger.info(f"Transcription saved to {output_file}")
            return transcription_text, output_file
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            raise
