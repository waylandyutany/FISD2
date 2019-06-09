from core.code import Code
from core.tokens import Tokens, TOKEN_NUMBER, TOKEN_STRING, TOKEN_NONE
from copy import deepcopy
from core.commands import ExecuteArgs
from core.code_line import Code_line

################################################################################
class Arguments(Tokens):
    def __init__(self, tokens):
        self._tokens = deepcopy(tokens.tokens()[:])

################################################################################
class Context:
    _variable_case_sensitive = False

    _CODE_NAME = 'code_name'
    _CODE_INDEX = 'code_index'
    _IF_STACK = 'if_stack'
    _VAR_STACK = 'var_stack'

    _VAR_TYPE = 'type'
    _VAR_VALUE = 'value'

    def __init__(self, code):
        self._code = code
        self._execution_stack = []
        self._logger = None

    @property
    def logger(self):
        return self._logger

################################################################################
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

    def __find_variable(self, name):
        if not Context._variable_case_sensitive:
            name = name.lower()

        var_stack = self._execution_stack[-1][Context._VAR_STACK]

        if name in var_stack:
            return var_stack[name][Context._VAR_TYPE], var_stack[name][Context._VAR_VALUE]
        return TOKEN_NONE, None

    def get_variable(self, name):
        type, value = self.__find_variable(name)
        return value

    def set_variable(self, name, value):
        if not Context._variable_case_sensitive:
            name = name.lower()

        var_stack = self._execution_stack[-1][Context._VAR_STACK]
        if isinstance(value, int):
            var_stack[name] = {Context._VAR_TYPE : TOKEN_NUMBER, Context._VAR_VALUE:value}
        elif isinstance(value, float):
            var_stack[name] = {Context._VAR_TYPE : TOKEN_NUMBER, Context._VAR_VALUE:value}
        else:
            var_stack[name] = {Context._VAR_TYPE : TOKEN_STRING, Context._VAR_VALUE:str(value)}

################################################################################
    def execute_code(self, code_name, call_stack_index = None):
        if call_stack_index == None:
            #creating code execution context
            execution_context = {Context._CODE_NAME:code_name, Context._CODE_INDEX:0, Context._IF_STACK:[], Context._VAR_STACK:{}}
            #pushing code context to the stack
            self._execution_stack.append(execution_context)
        else:
            pass #@todo take by the call_stack_index

        execute_args = ExecuteArgs(self)
        execute_args.code_name = execution_context[Context._CODE_NAME]

        #getting code lines from the code
        code_lines = self._code.get_code_lines(execute_args.code_name)

        #executing commands
        while execution_context[Context._CODE_INDEX] < len(code_lines):
            execute_args.code_line = code_lines[execution_context[Context._CODE_INDEX]]

            line_number, line_tokens, command_class = Code_line.split(execute_args.code_line)

            self.logger.preface = self._code.get_code_line_description(code_name, line_number)

            execute_args.arguments = self.__tokens_to_arguments(line_tokens)
            execute_args.code_lines = code_lines
            execute_args.code_index = execution_context[Context._CODE_INDEX]

            command_class.execute(execute_args)

            execution_context[Context._CODE_INDEX] += 1
            
        #popping code context from code stack
        self._execution_stack.pop()

    def jump_to_code(self, new_code_index):
        self._execution_stack[-1][Context._CODE_INDEX] = new_code_index - 1 # - 1 is due to #call_context[Context._CODE_INDEX] += 1 in execute_code loop!!!

################################################################################
    def begin_if(self):
        self._execution_stack[-1][Context._IF_STACK].append(False)

    def end_if(self):
        self._execution_stack[-1][Context._IF_STACK].pop()

    def skip_if(self):
        self._execution_stack[-1][Context._IF_STACK][-1] = True

    def is_skip_if(self):
        return self._execution_stack[-1][Context._IF_STACK][-1]

################################################################################
    def run(self, logger):
        self._logger = logger
        self.execute_code(self._code.main_code_name())

    def run_from_call_stack(self, call_stack, logger):
        pass

################################################################################

