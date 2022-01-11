import logging
from logging import getLogger, StreamHandler


def create_logger(log_level):
    level = getattr(logging, log_level.upper())
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = getLogger(__name__)
    logger.setLevel(level)
    logger.propagate = False

    err = StreamHandler()
    err.setLevel(level)
    err.setFormatter(formatter)
    logger.addHandler(err)

    return logger
