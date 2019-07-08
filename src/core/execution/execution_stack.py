from copy import deepcopy
from core.code.code_line import Code_line
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
    @property
    def is_empty(self):
        return len(self._stack) == 0

################################################################################
    @property
    def current_code_path(self):
        return self._code.code_name_to_code_path(self.current_code_name)

    @property
    def current_code_index(self):
        return self._stack[-1][Execution_stack._CODE_INDEX]

    @property
    def current_is_function(self):
        return self._stack[-1][Execution_stack._CODE_IS_FUNCTION]

    @property
    def current_code_name(self):
        return self._stack[-1][Execution_stack._CODE_NAME]

    @property
    def current_line_number(self):
        code_lines =  self._code.get_code_lines(self.current_code_name)
        return Code_line.get_line_number(code_lines[self.current_code_index])
