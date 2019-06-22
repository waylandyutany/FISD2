from core.utils import folder_and_file_name

################################################################################
class Code:
    _FUNCTION_FILE_NAME = 'function_file_name'
    _CODE_LINES = 'code_lines'

    def __init__(self):
        self._code = {}
        self._main_code_name = None

################################################################################
    def main_code_name(self):
        return self._main_code_name

    def get_code_lines(self, code_name):
        if code_name in self._code:
            return self._code[code_name][Code._CODE_LINES]
        return None

    def get_code_line_description(self, code_name, line_number):
        if Code._FUNCTION_FILE_NAME in self._code[code_name]:
            return "'{}'.'{}'[{:03d}] : ".format(folder_and_file_name(self._code[code_name][Code._FUNCTION_FILE_NAME]), code_name, line_number)
        return "'{}'[{:03d}] : ".format(folder_and_file_name(code_name), line_number)

    def is_code_function(self, code_name):
        return Code._FUNCTION_FILE_NAME in self._code[code_name]

################################################################################
