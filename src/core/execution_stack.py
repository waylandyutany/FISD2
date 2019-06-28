from copy import deepcopy
from core.code_line import Code_line
import os

################################################################################
class Execution_stack:
    _CODE_NAME = 'code_name'
    _CODE_INDEX = 'code_index'
    _CODE_IS_FUNCTION = 'is_function'

    def __init__(self, code):
        self._stack = []
        self._code = code

################################################################################
    def to_json_dict(self):
        return {'stack':deepcopy(self._stack)}

    def from_json_dict(self, json_dict):
        self._stack = json_dict['stack']

################################################################################
    def is_empty(self):
        return len(self._stack) == 0

################################################################################
    def __current_code_path(self):
        return self._code.code_name_to_code_path(self._stack[-1][Execution_stack._CODE_NAME])

    def current_code_index(self):
        return self._stack[-1][Execution_stack._CODE_INDEX]

    def current_is_function(self):
        return self._stack[-1][Execution_stack._CODE_IS_FUNCTION]

################################################################################
    def current_code_name(self):
        return self._stack[-1][Execution_stack._CODE_NAME]

    def current_file_name(self):
        return os.path.basename(self.__current_code_path())

    def current_file_folder(self):
        file_path, file_name = os.path.split(self.__current_code_path())
        _, file_folder = os.path.split(file_path)
        return file_folder

    def current_line_number(self):
        code_lines =  self._code.get_code_lines(self.current_code_name())
        return Code_line.get_line_number(code_lines[self.current_code_index()])
