import pytest
import os
from src.file_handler import FileHandler
from src.config import Config


@pytest.fixture
def file_handler():
    return FileHandler()


def test_validate_file_valid(file_handler):
    # Note: You'll need a test audio file
    test_audio = "path/to/test/audio.wav"
    if not os.path.exists(test_audio):
        pytest.skip("Test audio file not available")

    assert file_handler.validate_file(test_audio)


def test_validate_file_invalid(file_handler):
    with pytest.raises(FileNotFoundError):
        file_handler.validate_file("nonexistent_file.wav")

    with pytest.raises(ValueError):
        file_handler.validate_file("test.xyz")