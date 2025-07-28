import os
from src.file_handler import FileHandler
from src.transcriber import Transcriber
from src.utils import setup_logging, ensure_dir
from src.config import Config
import argparse


def main():
    parser = argparse.ArgumentParser(description="Audio/Video Transcription using OpenAI Whisper API")
    parser.add_argument("file_path", help="Path to audio or video file")
    parser.add_argument("--format", default="txt", choices=["txt", "srt"],
                        help="Output format for transcription")
    args = parser.parse_args()

    # Setup logging
    config = Config()
    ensure_dir(config.LOG_DIR)
    logger = setup_logging(config.LOG_FILE)

    try:
        file_handler = FileHandler()
        transcriber = Transcriber()

        # Validate input file
        file_handler.validate_file(args.file_path)

        # Handle video files
        _, ext = os.path.splitext(args.file_path)
        audio_path = args.file_path
        if ext.lower() in config.SUPPORTED_VIDEO_FORMATS:
            audio_path = os.path.join(
                config.OUTPUT_DIR,
                f"{os.path.basename(args.file_path).rsplit('.', 1)[0]}_audio.wav"
            )
            audio_path = file_handler.extract_audio_from_video(args.file_path, audio_path)

        # Convert to WAV if necessary
        audio_path = file_handler.convert_to_wav(audio_path)

        # Transcribe
        transcription, output_file = transcriber.transcribe(audio_path, args.format)
        print(f"Transcription completed. Output saved to: {output_file}")
        print("\nTranscription preview:")
        print(transcription[:500] + "..." if len(transcription) > 500 else transcription)

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
