import logging
import sys

_LOGGER = None

def get_logger(name: str = "qa"):
    """Uygulama genelinde kullanılacak logger"""
    global _LOGGER
    if _LOGGER is not None:
        return _LOGGER

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

    if not logger.handlers:
        logger.addHandler(handler)

    _LOGGER = logger
    return logger
