from copy import deepcopy

################################################################################
class Execution_stack:
    _CODE_NAME = 'code_name'
    _CODE_INDEX = 'code_index'
    _CODE_IS_FUNCTION = 'is_function'

    def __init__(self):
        self._stack = []

################################################################################
    def to_json_dict(self):
        return {'stack':deepcopy(self._stack)}

    def from_json_dict(self, json_dict):
        self._stack = json_dict['stack']

################################################################################
    def is_empty(self):
        return len(self._stack) == 0

################################################################################
    def current_code_name(self):
        return self._stack[-1][Execution_stack._CODE_NAME]

    def __current_code_path(self):
        return self._code.code_name_to_code_path(self._stack[-1][Execution_stack._CODE_NAME])

    def current_file_name(self):
        return os.path.basename(self.__current_code_path(self))

    def current_file_folder(self):
        file_path, file_name = os.path.split(self.__current_code_path(self))
        _, file_folder = os.path.split(file_path)
        return file_folder

    #@todo finish this
    #def current_line_number(self):
    #    return 0
