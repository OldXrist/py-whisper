import os
from src.file_handler import FileHandler
from src.chunker import AudioChunker
from src.transcriber import Transcriber
from src.utils import setup_logging, ensure_dir
from src.config import Config
import argparse


def main():
    parser = argparse.ArgumentParser(description="Audio/Video Transcription using Groq Whisper API")
    parser.add_argument("file_path", help="Path to audio or video file")
    parser.add_argument("--format", default="verbose_json", help="Output format for transcription")
    args = parser.parse_args()

    # Setup logging
    config = Config()
    ensure_dir(config.LOG_DIR)
    logger = setup_logging(config.LOG_FILE)

    try:
        file_handler = FileHandler()
        chunker = AudioChunker()
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

        # Split audio if necessary
        audio_chunks = chunker.split_audio(audio_path)

        # Transcribe chunks
        full_transcription = ""
        output_files = []
        for i, chunk_path in enumerate(audio_chunks):
            logger.info(f"Processing chunk {i + 1}/{len(audio_chunks)}")
            transcription, output_file = transcriber.transcribe(chunk_path, args.format)
            full_transcription += transcription + "\n" if args.format == "txt" else transcription + "\n\n"
            output_files.append(output_file)

        # Combine transcriptions into a single file
        combined_output = os.path.join(
            config.OUTPUT_DIR,
            f"{os.path.basename(args.file_path).rsplit('.', 1)[0]}_combined.{args.format}"
        )
        with open(combined_output, "w", encoding="utf-8") as f:
            f.write(full_transcription.strip())

        print(f"Transcription completed. Combined output saved to: {combined_output}")
        print("\nTranscription preview:")
        print(full_transcription[:500] + "..." if len(full_transcription) > 500 else full_transcription)

        # Clean up chunk files (optional)
        for chunk_path in audio_chunks:
            if chunk_path != audio_path:  # Don't delete the original audio
                try:
                    os.remove(chunk_path)
                    logger.info(f"Cleaned up chunk: {chunk_path}")
                except Exception as e:
                    logger.warning(f"Failed to clean up chunk {chunk_path}: {str(e)}")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
