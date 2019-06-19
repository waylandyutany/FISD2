from core.code import Code
from core.commands import Commands
from core.code_line import Code_line
from copy import deepcopy

################################################################################
class Code_json(Code):
    def to_json_dict(self):
        code_dict = deepcopy(self._code)
        for code_name in code_dict:
            code_lines = code_dict[code_name][Code._CODE_LINES]
            for code_line in code_lines:
                code_line[Code_line._TOKENS] = code_line[Code_line._TOKENS]._tokens
                code_line[Code_line._COMMAND_CLASS] = code_line[Code_line._COMMAND_CLASS]._keyword

        return {'_code':code_dict, '_main_code_name':self._main_code_name}

    def from_json_dict(self, code_json):
        pass
