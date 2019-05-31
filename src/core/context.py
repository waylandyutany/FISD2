from core.code import Code
from core.tokens import Tokens, TOKEN_NUMBER, TOKEN_STRING, TOKEN_NONE
from copy import deepcopy

################################################################################
class Arguments(Tokens):
    def __init__(self, tokens):
        self._tokens = deepcopy(tokens.tokens()[:])

################################################################################
class Context:
    _CODE_NAME = 'code_name'
    _CODE_INDEX = 'code_index'
    _VAR_TYPE = 'type'
    _VAR_VALUE = 'value'

    def __init__(self, code):
        self._code = code
        self._call_stack = []
        self._variable_stack = [{}]
        self._logger = None

    @property
    def logger(self):
        return self._logger

    def __tokens_to_arguments(self, tokens):
        args =  Arguments(tokens)
        for i in range(0, len(args)):
            if args.is_name(i):
                type, value = self.__find_variable(args.value(i))
                if type == TOKEN_NUMBER:
                    args.set_number(i, value)
                elif type == TOKEN_STRING:
                    args.set_string(i, value)

        return args

################################################################################
    def __find_variable(self, name):
        if name in self._variable_stack[-1]:
            return self._variable_stack[-1][name][Context._VAR_TYPE], self._variable_stack[-1][name][Context._VAR_VALUE]
        return TOKEN_NONE, None

    def set_variable(self, name, value):
        if isinstance(value, int):
            self._variable_stack[-1][name] = {Context._VAR_TYPE : TOKEN_NUMBER, Context._VAR_VALUE:value}
        elif isinstance(value, float):
            self._variable_stack[-1][name] = {Context._VAR_TYPE : TOKEN_NUMBER, Context._VAR_VALUE:value}
        else:
            self._variable_stack[-1][name] = {Context._VAR_TYPE : TOKEN_STRING, Context._VAR_VALUE:str(value)}

################################################################################
    def execute_code(self, code_name, call_stack_index = None):
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

            self.logger.preface = "'{}'[{}] : ".format(code_name, line_number)

            command_class.execute(self, self.__tokens_to_arguments(line_tokens))
            
        #popping code context from code stack
        self._call_stack.pop()

################################################################################
    def run(self, logger):
        self._logger = logger
        self.execute_code(self._code.main_code_name(), logger)

    def run_from_call_stack(self, call_stack, logger):
        pass

################################################################################

