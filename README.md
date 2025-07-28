# py-whisper

A Python application for transcribing audio and video files using OpenAI's Whisper API.

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure FFmpeg is installed on your system
4. Create a `.env` file in the project root and configure it (see `.env` section below)

## .env Configuration
Rename the `.env.dest` to `.env` with the following variables:
```bash
OPENAI_API_KEY=your_openai_api_key_here
WHISPER_MODEL=whisper-1
SUPPORTED_AUDIO_FORMATS=.wav,.mp3,.m4a
SUPPORTED_VIDEO_FORMATS=.mp4,.avi,.mov
OUTPUT_DIR=transcriptions
LOG_DIR=logs
LOG_FILE=transcription.log