import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys

################################################################################
class Logger:
    format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_log_handler = logging.StreamHandler(sys.stdout)
    file_log_handler = handlers.RotatingFileHandler("fisd2.log", maxBytes=(1 * 1024 * 1024), backupCount=1)
    log = logging.getLogger('fisd2_logger')

    @classmethod
    def init_logger(cls, name = 'fisd2_loger'):
        cls.log.setLevel(logging.DEBUG)
        #cls.console_log_handler.setFormatter(cls.format)
        cls.file_log_handler.setFormatter(cls.format)

        cls.log.addHandler(cls.console_log_handler)
        cls.log.addHandler(cls.file_log_handler)

################################################################################
    def __init__(self):
        pass
       