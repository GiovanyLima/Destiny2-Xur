import sys

from loguru import logger

fmt = "<lvl>[{time:MMMM D, YYYY -> HH:mm:ss}] | {level} | {file} | {function}:{line} | {message}</lvl>"


def setup_logging():
    logger.remove(0)
    logger.add(
        sys.stdout,
        format=fmt,
    )
    logger.add(
        "logs.log",
        format=fmt,
    )
    logger.success("Logging configurado com sucesso!")
