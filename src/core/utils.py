from datetime import datetime

class TimeLogger:
    def __init__(self, message, logger):
        self._message = message
        self._logger = logger

    def __enter__(self):
        self._start_time = datetime.now()

    def __exit__(self, type, value, tb):
        delta_time = datetime.now() - self._start_time
        self._logger.info("{} '{}'.".format(self._message, delta_time))

