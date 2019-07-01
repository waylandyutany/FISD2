import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys
from termcolor import colored
################################################################################
class Logger:
    file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_log_handler = handlers.RotatingFileHandler("fisd2.log", maxBytes=(1 * 1024 * 1024), backupCount=1)

    console_format = logging.Formatter("%(levelname)s - %(message)s")
    console_log_handler = logging.StreamHandler(sys.stdout)

    log = logging.getLogger('fisd2_logger')

    _KEY_DEBUG = 'DBG'
    _KEY_INFO = 'INF'
    _KEY_WARNING = 'WRN'
    _KEY_ERROR = 'ERR'
    _KEY_CRITICAL = 'CRITICAL'

    _COLOR_DEBUG = 'white'
    _COLOR_INFO = 'white'
    _COLOR_WARNING = 'yellow'
    _COLOR_ERROR = 'red'
    _COLOR_CRITICAL = 'red'

    @classmethod
    def init_logger(cls, name = 'fisd2_logger'):
        cls.log.setLevel(logging.DEBUG)

        logging.addLevelName(logging.ERROR, cls._KEY_ERROR)
        logging.addLevelName(logging.INFO, cls._KEY_INFO)
        logging.addLevelName(logging.DEBUG, cls._KEY_DEBUG)
        logging.addLevelName(logging.WARNING, cls._KEY_WARNING)
        logging.addLevelName(logging.CRITICAL, cls._KEY_CRITICAL)

        cls.console_log_handler.setFormatter(cls.console_format)
        cls.file_log_handler.setFormatter(cls.file_format)

        #cls.log.addHandler(cls.console_log_handler)
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

        print(colored("{} - {}".format(Logger._KEY_DEBUG, msg), Logger._COLOR_DEBUG))

        if self._log:
            self._log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        msg = self.preface + str(msg)

        print(colored("{} - {}".format(Logger._KEY_INFO, msg), Logger._COLOR_INFO))

        if self._log:
            self._log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        msg = self.preface + str(msg)

        self._warnings += 1

        print(colored("{} - {}".format(Logger._KEY_WARNING, msg), Logger._COLOR_WARNING))

        if self._log:
            self._log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        msg = self.preface + str(msg)

        self._errors += 1

        print(colored("{} - {}".format(Logger._KEY_ERROR, msg), Logger._COLOR_ERROR))

        if self._log:
            self._log.error(msg, *args, **kwargs)

    def reset_errors(self):
        self._errors = 0

    def critical(self, msg, *args, **kwargs):
        msg = self.preface + str(msg)

        self._criticals += 1

        print(colored("{} - {}".format(Logger._KEY_CRITICAL, msg), Logger._COLOR_CRITICAL))

        if self._log:
            self._log.critical(msg, *args, **kwargs)
