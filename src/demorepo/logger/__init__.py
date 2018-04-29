import logging
from demorepo import strformat

__all__ = ["info", "error", "add_console_handler", "add_file_handler"]

logger = logging.getLogger("demorepo")

# Set log level to INFO
logger.setLevel(logging.INFO)

# Ensure that the logger has no handlers
logger.handlers.clear()


def info(text, color=None):
    logger.info(strformat.format(text, color=color))


def error(text):
    logger.error(strformat.format(text, color=strformat.RED))


def add_console_handler():
    # Add the console handler. Just prints the message
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)


def add_file_handler(path):
    # Add the console handler. Just prints the message
    fh = logging.FileHandler(path)
    fh.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(fh)
