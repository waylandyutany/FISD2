from datetime import datetime
import os

################################################################################
class TimeLogger:
    def __init__(self, pre_msg, post_msg, logger_func):
        self._pre_msg = pre_msg
        self._post_msg = post_msg

        self._logger_func = logger_func

    def __enter__(self):
        self._start_time = datetime.now()
        self._logger_func("{}".format(self._pre_msg))

    def __exit__(self, type, value, tb):
        delta_time = datetime.now() - self._start_time
        self._logger_func("{} {}s.".format(self._post_msg, delta_time.total_seconds()))

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

