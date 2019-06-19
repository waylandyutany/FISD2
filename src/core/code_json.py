from core.code import Code
from core.commands import Commands
from core.code_line import Code_line
from copy import deepcopy
from core.tokens import Tokens

################################################################################
class Code_json(Code):
    def to_json_dict(self):
        code_dict = deepcopy(self._code)
        for code_name in code_dict:
            code_lines = code_dict[code_name][Code._CODE_LINES]
            for code_line in code_lines:
                code_line[Code_line._TOKENS] = code_line[Code_line._TOKENS]._tokens
                code_line[Code_line._COMMAND_CLASS] = code_line[Code_line._COMMAND_CLASS]._keyword

        return {'_code':code_dict,
                '_main_code_name':self._main_code_name}

    #@todo error when no command class available
    #@todo add version
    def from_json_dict(self, json_dict, logger):
        self._main_code_name, code_dict = json_dict['_main_code_name'], json_dict['_code']

        for code_name in code_dict:
            code_lines = code_dict[code_name][Code._CODE_LINES]
            for code_line in code_lines:
                tokens = Tokens("")
                tokens._tokens = code_line[Code_line._TOKENS]
                code_line[Code_line._TOKENS] = tokens
                code_line[Code_line._COMMAND_CLASS] = Commands.find_command(code_line[Code_line._COMMAND_CLASS])

        self._code = code_dict
