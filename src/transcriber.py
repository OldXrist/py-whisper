from groq import Groq
from .config import Config
from .utils import logger, ensure_dir
import os


class Transcriber:
    def __init__(self):
        config = Config()
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.WHISPER_MODEL
        logger.info(f"Groq Whisper API model '{self.model}' initialized")


    def transcribe(self, audio_path, output_format="txt"):
        try:
            config = Config()
            logger.info(f"Starting transcription of {audio_path}")
            with open(audio_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=(os.path.basename(audio_path), audio_file.read()),
                    response_format="verbose_json"
                )

            transcription_text = transcription.text

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
