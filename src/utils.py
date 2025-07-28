from loguru import logger
import os


def setup_logging(log_file):
    logger.add(log_file, rotation="10 MB", retention="7 days")
    return logger


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
