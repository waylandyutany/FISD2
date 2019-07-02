import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys
from copy import copy
from termcolor import colored

################################################################################
class ColoredFormatter(logging.Formatter):
    level_to_color = {
        logging.DEBUG : 'white',
        logging.INFO : 'white',
        logging.WARNING : 'yellow',
        logging.ERROR : 'red',
        logging.CRITICAL : 'red'
    }

    def __init__(self, patern):
        logging.Formatter.__init__(self, patern)

    def format(self, record):
        colored_record = copy(record)
        colored_record.levelname = "{}".format(colored(colored_record.levelname, ColoredFormatter.level_to_color[colored_record.levelno]))
        #colored_record.msg
        return logging.Formatter.format(self, colored_record)

################################################################################
class Logger:
    file_log_handler = None
    console_log_handler = None

    log = logging.getLogger('fisd2_logger')

    _KEY_DEBUG = 'DBG'
    _KEY_INFO = 'INF'
    _KEY_WARNING = 'WRN'
    _KEY_ERROR = 'ERR'
    _KEY_CRITICAL = 'CRITICAL'

    @classmethod
    def init_logger(cls, log_file_name, log_verbosity):
        if log_file_name:
            cls.file_log_handler = handlers.RotatingFileHandler(log_file_name, maxBytes=(1 * 1024 * 1024), backupCount=1)

        cls.console_log_handler = logging.StreamHandler(sys.stdout)

        log_verbosity = str(log_verbosity).upper()
        if hasattr(logging, log_verbosity):
            cls.log.setLevel(getattr(logging, log_verbosity))
        else:
            cls.log.setLevel(logging.INFO)

        logging.addLevelName(logging.ERROR, cls._KEY_ERROR)
        logging.addLevelName(logging.INFO, cls._KEY_INFO)
        logging.addLevelName(logging.DEBUG, cls._KEY_DEBUG)
        logging.addLevelName(logging.WARNING, cls._KEY_WARNING)
        logging.addLevelName(logging.CRITICAL, cls._KEY_CRITICAL)

        if cls.file_log_handler:
            cls.file_log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            cls.log.addHandler(cls.file_log_handler)

        if cls.console_log_handler:
            cls.console_log_handler.setFormatter(ColoredFormatter("%(levelname)s - %(message)s"))
            cls.log.addHandler(cls.console_log_handler)
    
################################################################################
    def __init__(self, log = None):
        self._criticals = 0
        self._errors = 0
        self._warnings = 0
        self._log = log
        self.preface = ""
       
    def message(self, msg):
        return self.preface + str(msg) 

################################################################################
    def reset_criticals(self):
        self._criticals = 0

    def reset_errors(self):
        self._errors = 0

    def reset_warnings(self):
        self._warnings = 0

################################################################################
    def debug(self, msg, *args, **kwargs):
        if self._log:
            self._log.debug(self.message(msg), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self._log:
            self._log.info(self.message(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._warnings += 1

        if self._log:
            self._log.warning(self.message(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._errors += 1

        if self._log:
            self._log.error(self.message(msg), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._criticals += 1

        if self._log:
            self._log.critical(self.message(msg), *args, **kwargs)
