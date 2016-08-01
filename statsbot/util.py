"""statsbot.util module."""

import logging


def prepare_logger(level):
    """Configure logging for the module."""
    logger = logging.getLogger(__package__)
    logger.setLevel(getattr(logging, level))

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        datefmt='%Y/%m/%d %H:%M:%S',
        fmt='%(asctime)s %(levelname)-5s %(message)s'))
    logger.addHandler(handler)
    return logger
