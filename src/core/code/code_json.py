from core.code.code import Code
from core.code.code_line import Code_line
from core.commands import Commands
from copy import deepcopy
from core.tokens import Tokens

################################################################################
class Code_json(Code):
    __JSON_VERSION__ = 0

    def to_json_dict(self):
        code_dict = deepcopy(self._code)
        for code_name in code_dict:
            code_lines = code_dict[code_name][Code._CODE_LINES]
            for code_line in code_lines:
                code_line[Code_line._TOKENS] = code_line[Code_line._TOKENS]._tokens
                code_line[Code_line._COMMAND_CLASS] = code_line[Code_line._COMMAND_CLASS]._keyword

        return {'code':code_dict,
                'main_code_name':self._main_code_name,
                'json_version':Code_json.__JSON_VERSION__}

    #@todo error when no command class available
    #@todo add version
    def from_json_dict(self, json_dict, logger):
        self._main_code_name, code_dict, json_version = json_dict['main_code_name'], json_dict['code'], json_dict['json_version']

        for code_name in code_dict:
            code_lines = code_dict[code_name][Code._CODE_LINES]
            for code_line in code_lines:
                code_line[Code_line._TOKENS] = Tokens(code_line[Code_line._TOKENS])
                code_line[Code_line._COMMAND_CLASS] = Commands.find_command(code_line[Code_line._COMMAND_CLASS])

        self._code = code_dict
