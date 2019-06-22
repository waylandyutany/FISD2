from datetime import datetime
import os

################################################################################
class TimeLogger:
    def __init__(self, message, logger):
        self._message = message
        self._logger = logger

    def __enter__(self):
        self._start_time = datetime.now()

    def __exit__(self, type, value, tb):
        delta_time = datetime.now() - self._start_time
        self._logger.info("{} '{}'.".format(self._message, delta_time))

################################################################################
class PrefaceLogger:
    def __init__(self, new_preface, logger):
        self._logger = logger
        self._previous_preface = self._logger.preface
        self._logger.preface = new_preface

    def __enter__(self):
        pass

    def __exit__(self, type, value, tb):
        self._logger.preface = self._previous_preface

################################################################################
def folder_and_file_name(file_path):
    ''' Return file name with it's root folder name'''
    file_path, file_name = os.path.split(file_path)
    _, file_folder = os.path.split(file_path)
    return os.path.join(file_folder, file_name)

