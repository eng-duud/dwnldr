import logging
import os
from config import LOG_PATH

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

logging.basicConfig(
    level=logging.INFO,
    format=
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_PATH, 'bot.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
