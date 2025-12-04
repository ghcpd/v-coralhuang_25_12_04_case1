import logging

logger = logging.getLogger("user_display")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def debug(msg, **kwargs):
    logger.debug(f"{msg} | {kwargs}")

def info(msg, **kwargs):
    logger.info(f"{msg} | {kwargs}")

def error(msg, **kwargs):
    logger.error(f"{msg} | {kwargs}")
