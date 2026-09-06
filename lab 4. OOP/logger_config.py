import logging
from logging.handlers import RotatingFileHandler


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] (%(name)s): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler('app.log', maxBytes=5 * 1024 * 1024, backupCount=3, encoding='utf-8')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger
