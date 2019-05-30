from core.code import Code
from core.tokens import Tokens
from copy import deepcopy

################################################################################
class Arguments(Tokens):
    def __init__(self, tokens):
        self._tokens = deepcopy(tokens.tokens()[:])

################################################################################
class Context:
    _CODE_NAME = 'code_name'
    _CODE_INDEX = 'code_index'

    def __init__(self, code):
        self._code = code
        self._call_stack = []
        self._variable_stack = [{}]

    def __tokens_to_arguments(self, tokens):
        return Arguments(tokens)

################################################################################
    def execute_code(self, code_name, logger, call_stack_index = None):
        #getting code lines from the code
        code_lines = self._code.get_code_lines(code_name)

        #creating code context
        call_context = {Context._CODE_NAME:code_name, Context._CODE_INDEX:0}

        #pushing code context to the stack
        self._call_stack.append(call_context)

        #executing commands
        for code_index in range(call_context[Context._CODE_INDEX], len(code_lines)):
            call_context[Context._CODE_INDEX] = code_index

            line_number, line_tokens, command_class = Code.split_code_line(code_lines[code_index])

            logger.preface = "'{}'[{}] : ".format(code_name, line_number)

            command_class.execute(self, self.__tokens_to_arguments(line_tokens), logger)
            
        #popping code context from code stack
        self._call_stack.pop()

################################################################################
    def run(self, logger):
        self.execute_code(self._code.main_code_name(), logger)

    def run_from_call_stack(self, call_stack, logger):
        pass
################################################################################
    def set_variable(self, name, value):
        self._variable_stack[-1][name] = value