import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', 'downloads')
LOG_PATH = os.getenv('LOG_PATH', 'logs')
TEMP_PATH = os.getenv('TEMP_PATH', 'temp')
