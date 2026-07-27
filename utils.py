import re
import os
import shutil
from urllib.parse import urlparse
from config import DOWNLOAD_PATH, TEMP_PATH, LOG_PATH
from logger import logger

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def clean_up_files(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            logger.info(f"Cleaned up directory: {path}")
        else:
            os.remove(path)
            logger.info(f"Cleaned up file: {path}")

def create_directories():
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(TEMP_PATH, exist_ok=True)
    os.makedirs(LOG_PATH, exist_ok=True)
    logger.info("Ensured all necessary directories exist.")

def sanitize_filename(filename):
    # Remove invalid characters for filenames
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Trim leading/trailing spaces and periods
    filename = filename.strip(' .')
    return filename

# Placeholder for progress callback - will be implemented in handlers.py
def download_progress_hook(d):
    if d['status'] == 'downloading':
        # This will be updated to send progress to Telegram
        pass
    elif d['status'] == 'finished':
        logger.info(f"Finished downloading {d['filename']}")
