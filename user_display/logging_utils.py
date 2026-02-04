import logging
import json


def setup_logger(name: str = __name__, level=logging.INFO):
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        h.setFormatter(fmt)
        logger.addHandler(h)
    logger.setLevel(level)
    return logger


def structured_log(logger, event: str, **kwargs):
    payload = {"event": event}
    payload.update(kwargs)
    logger.info(json.dumps(payload))
