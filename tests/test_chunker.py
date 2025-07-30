import pytest
import os
from src.chunker import AudioChunker
from src.config import Config


@pytest.fixture
def chunker():
    return AudioChunker()


def test_split_audio_small_file(chunker, tmp_path):
    # Note: You'll need a small test audio file
    test_audio = "path/to/test/small_audio.wav"
    if not os.path.exists(test_audio):
        pytest.skip("Test audio file not available")

    chunks = chunker.split_audio(test_audio)
    assert len(chunks) == 1
    assert chunks[0] == test_audio


def test_split_audio_large_file(chunker, tmp_path):
    # Note: You'll need a large test audio file
    test_audio = "path/to/test/large_audio.wav"
    if not os.path.exists(test_audio):
        pytest.skip("Test audio file not available")

    chunks = chunker.split_audio(test_audio)
    assert len(chunks) > 1
    for chunk in chunks:
        assert os.path.exists(chunk)
        assert os.path.getsize(chunk) / (1024 * 1024) <= Config().MAX_CHUNK_SIZE_MB