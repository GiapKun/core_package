import logging
import sys
from typing import Optional


class CustomFormatter(logging.Formatter):
    """Custom log formatter with color support."""

    grey = "\x1b[38;21m"
    green = "\x1b[32m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    base_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + base_format + reset,
        logging.INFO: green + base_format + reset,
        logging.WARNING: yellow + base_format + reset,
        logging.ERROR: red + base_format + reset,
        logging.CRITICAL: bold_red + base_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.base_format)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger(name: str, level: int = logging.INFO, formatter: Optional[logging.Formatter] = None) -> logging.Logger:
    """
    Sets up a logger with the given name, level, and formatter.

    Args:
        name (str): Name of the logger.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        formatter (Optional[logging.Formatter]): Custom formatter for the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(formatter or CustomFormatter())
        logger.addHandler(handler)

    return logger
