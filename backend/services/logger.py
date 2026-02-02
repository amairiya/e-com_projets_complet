# logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

# Création du dossier logs si inexistant
os.makedirs("logs", exist_ok=True)

# Logger global
logger = logging.getLogger("bijoux_glam_logger")
logger.setLevel(logging.INFO)



# Récupère la date du jour au format YYYY-MM-DD
today = datetime.now().strftime("%Y-%m-%d")

# Fichier de log incluant la date
log_file = f"logs/app_{today}.log"

handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, backupCount=30, encoding="utf-8"
)
handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

# def log(message, level="INFO", order_number=None):
#     """Log dans le fichier avec rotation quotidienne"""
#     order_info = f" | Order: {order_number}" if order_number else ""
#     full_message = f"{message}{order_info}"

#     if level.upper() == "INFO":
#         logger.info(full_message)
#     elif level.upper() == "WARNING":
#         logger.warning(full_message)
#     elif level.upper() == "ERROR":
#         logger.error(full_message)
#     else:
#         logger.info(full_message)


def log(message, level="INFO", order_number=None, ip=None, path=None, method=None, status=None, duration_ms=None):
    parts = [str(message)]   # 👈 FIX CRITIQUE

    if ip:
        parts.append(f"ip={ip}")
    if method:
        parts.append(f"method={method}")
    if path:
        parts.append(f"path={path}")
    if status:
        parts.append(f"status={status}")
    if duration_ms:
        parts.append(f"duration_ms={duration_ms}")
    if order_number:
        parts.append(f"order_number={order_number}")

    full_message = " | ".join(parts)

    level = level.upper()
    if level == "INFO":
        logger.info(full_message)
    elif level == "WARNING":
        logger.warning(full_message)
    elif level == "ERROR":
        logger.error(full_message)
    else:
        logger.info(full_message)

        



