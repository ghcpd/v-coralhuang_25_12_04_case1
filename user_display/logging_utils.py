"""Small structured logging helpers for the package."""
import logging


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def debug(msg, *args, **kwargs):
    get_logger().debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    get_logger().info(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    get_logger().warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    get_logger().error(msg, *args, **kwargs)
