"""statsbot.util module."""

import logging


def prepare_logger(level):
    """Configure logging for the module."""
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        datefmt='%Y/%m/%d %H:%M:%S',
        fmt='%(asctime)s %(levelname)-5s %(message)s'))

    stats_logger = logging.getLogger(__package__)
    prawtools_logger = logging.getLogger('prawtools')

    for logger in (stats_logger, prawtools_logger):
        logger.setLevel(getattr(logging, level))
        logger.addHandler(handler)
    return stats_logger
