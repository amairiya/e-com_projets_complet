# logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Création du dossier logs si inexistant
os.makedirs("logs", exist_ok=True)

# Logger global
logger = logging.getLogger("bijoux_glam_logger")
logger.setLevel(logging.INFO)

# Handler pour rotation quotidienne
log_file = "logs/app.log"
handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, backupCount=30, encoding="utf-8"
)
handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

def log(message, level="INFO", order_number=None):
    """Log dans le fichier avec rotation quotidienne"""
    order_info = f" | Order: {order_number}" if order_number else ""
    full_message = f"{message}{order_info}"

    if level.upper() == "INFO":
        logger.info(full_message)
    elif level.upper() == "WARNING":
        logger.warning(full_message)
    elif level.upper() == "ERROR":
        logger.error(full_message)
    else:
        logger.info(full_message)
