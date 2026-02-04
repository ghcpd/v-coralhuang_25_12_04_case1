import logging
import json

logger = logging.getLogger('user_display')
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)


def log_structured(level, event, **kwargs):
    data = {'event': event}
    data.update(kwargs)
    logger.log(level, json.dumps(data))
