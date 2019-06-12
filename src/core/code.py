import core.code_keys as code_keys

################################################################################
class Code:
    _FUNCTION_FILE_NAME = 'function_file_name'
    _CODE_LINES = 'code_lines'

    def __init__(self):
        self._code = {}
        self._main_code_name = None

    def load_from_file(self, file_name, logger):
        ''' Loading already compiled code from the file.'''

    def save_to_file(self, file_name, logger):
        ''' Saving compiled code to the file.'''

################################################################################
    def main_code_name(self):
        return self._main_code_name

    def get_code_lines(self, code_name):
        if code_name in self._code:
            return self._code[code_name][Code._CODE_LINES]
        return None

    def get_code_line_description(self, code_name, line_number):
        if Code._FUNCTION_FILE_NAME in self._code[code_name]:
            return "'{}'.'{}'[{:03d}] : ".format(self._code[code_name][Code._FUNCTION_FILE_NAME], code_name, line_number)
        return "'{}'[{:03d}] : ".format(code_name, line_number)

################################################################################
