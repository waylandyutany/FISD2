import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys

################################################################################
class Logger:
    file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_format = logging.Formatter("%(levelname)s - %(message)s")
    console_log_handler = logging.StreamHandler(sys.stdout)
    file_log_handler = handlers.RotatingFileHandler("fisd2.log", maxBytes=(1 * 1024 * 1024), backupCount=1)
    log = logging.getLogger('fisd2_logger')

    @classmethod
    def init_logger(cls, name = 'fisd2_loger'):
        cls.log.setLevel(logging.DEBUG)
        cls.console_log_handler.setFormatter(cls.console_format)
        cls.file_log_handler.setFormatter(cls.file_format)

        cls.log.addHandler(cls.console_log_handler)
        cls.log.addHandler(cls.file_log_handler)

################################################################################
    def __init__(self, log = None):
        self._criticals = 0
        self._errors = 0
        self._warnings = 0
        self._log = log
        self.preface = ""
       
    def debug(self, msg, *args, **kwargs):
        msg = self.preface + str(msg)
        if self._log:
            self._log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        msg = self.preface + str(msg)
        if self._log:
            self._log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        msg = self.preface + str(msg)
        self._warnings += 1
        if self._log:
            self._log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        msg = self.preface + str(msg)
        self._errors += 1
        if self._log:
            self._log.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        msg = self.preface + str(msg)
        self._criticals += 1
        if self._log:
            self._log.critical(msg, *args, **kwargs)
