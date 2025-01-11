import json
import logging
import os
import sys

from loguru import logger
from datetime import timedelta
from test_genie.core.configs import config


def setup_logging():
    logger.remove()

    # create logs directory if not exists
    log_path = 'logs'
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')

    class LoguruHandler(logging.Handler):
        def emit(self, record):
            logger.opt(depth=6).log(record.levelno, record.getMessage())

    sqlalchemy_logger.addHandler(LoguruHandler())

    log_config = {
        "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                  "<level>{level: <8}</level> | "
                  "<level>{message}</level>",
        "level": config.LOG_LEVEL,
    }

    # local env
    logger.add(sys.stdout, colorize=True, **log_config)
    logger.add(os.path.join(log_path, "{time}.log"), rotation=timedelta(days=1), **log_config)
