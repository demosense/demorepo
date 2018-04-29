import logging
from demorepo import strformat

__all__ = ["info", "error"]

logger = logging.getLogger("demorepo")

# Set log level to INFO
logger.setLevel(logging.INFO)

# Ensure that the logger has no handlers
logger.handlers.clear()

# Add the console handler. Just prints the message
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(ch)


def info(text):
    logger.info(strformat.format(text))


def error(text):
    logger.error(strformat.format(text, color=strformat.RED))
