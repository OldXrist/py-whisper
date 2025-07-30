import pytest
import os
from src.transcriber import Transcriber


@pytest.fixture
def transcriber():
    return Transcriber()


def test_transcription(transcriber, tmp_path):
    # Note: You'll need a test audio file
    test_audio = "test_files/audio.wav"
    if not os.path.exists(test_audio):
        pytest.skip("Test audio file not available")

    transcription, output_file = transcriber.transcribe(test_audio)
    assert isinstance(transcription, str)
    assert os.path.exists(output_file)
    assert output_file.endswith(".txt")