from core.code import Code
from core.tokens import Tokens, TOKEN_NUMBER, TOKEN_STRING, TOKEN_NONE
from copy import deepcopy
from core.commands import ExecuteArgs
from core.code_line import Code_line
from core.utils import PrefaceLogger
import json, os

from default_commands.fisd_commands import Fisd_restore_context_command

################################################################################
class Arguments(Tokens):
    def __init__(self, tokens):
        self._tokens = deepcopy(tokens.tokens()[:])

################################################################################
class Context:
    _variable_case_sensitive = False

    _CODE_NAME = 'code_name'
    _CODE_INDEX = 'code_index'
    _CODE_IS_FUNCTION = 'is_function'

    _VAR_TYPE = 'type'
    _VAR_VALUE = 'value'

    def __init__(self, code, logger):
        self._code = code

        self._call_tokens = None
        self._return = None
        self._exit = False

        self._logger = logger

        self._execution_stack = []
        self._variable_stack = [{}]

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

        var_stack = self._variable_stack[-1]
        if name in var_stack:
            return var_stack[name][Context._VAR_TYPE], var_stack[name][Context._VAR_VALUE]

        if len(self._variable_stack) > 1:
            global_var_stack = self._variable_stack[0]
            if name in global_var_stack:
                return global_var_stack[name][Context._VAR_TYPE], global_var_stack[name][Context._VAR_VALUE]

        return TOKEN_NONE, None

    def get_variable(self, name):
        type, value = self.__find_variable(name)
        return value

    def set_variable(self, name, value):
        if not Context._variable_case_sensitive:
            name = name.lower()

        var_stack = self._variable_stack[-1]

        if isinstance(value, int):
            var_stack[name] = {Context._VAR_TYPE : TOKEN_NUMBER, Context._VAR_VALUE:value}
        elif isinstance(value, float):
            var_stack[name] = {Context._VAR_TYPE : TOKEN_NUMBER, Context._VAR_VALUE:value}
        else:
            var_stack[name] = {Context._VAR_TYPE : TOKEN_STRING, Context._VAR_VALUE:str(value)}

################################################################################
    def execute_code(self, code_name, execution_stack_index = None):
        # creating new execution context and pushing it into execution stack
        if execution_stack_index == None:
            #creating code execution context
            execution_context = {Context._CODE_NAME:code_name,
                                 Context._CODE_INDEX:0,
                                 Context._CODE_IS_FUNCTION:self._code.is_code_function(code_name)}
            #pushing code context to the stack
            self._execution_stack.append(execution_context)
            #if function call new var stack is pushed
            if execution_context[Context._CODE_IS_FUNCTION]:
                self._variable_stack.append({})
        else:# restoring execution context from execution stack recurrently
            execution_context = self._execution_stack[execution_stack_index]
            if execution_stack_index + 1 < len(self._execution_stack):
                self.execute_code(code_name, execution_stack_index + 1)
            else:# in case of last execution context, we search for restoration point code line
                 # so code will start from that point
                code_lines = self._code.get_code_lines(execution_context[Context._CODE_NAME])
                while execution_context[Context._CODE_INDEX] < len(code_lines):
                    cmd_class = Code_line.get_command_class(code_lines[execution_context[Context._CODE_INDEX]])
                    if cmd_class._keyword == Fisd_restore_context_command._keyword:
                        break
                    execution_context[Context._CODE_INDEX] += 1

        #getting code lines from the code
        code_lines = self._code.get_code_lines(execution_context[Context._CODE_NAME])
        execute_args = ExecuteArgs(self, self._logger, execution_context[Context._CODE_NAME], code_lines)

        #executing commands
        while execution_context[Context._CODE_INDEX] < len(code_lines) and (self._exit == False):
            execute_args.code_line = code_lines[execution_context[Context._CODE_INDEX]]

            line_number, line_tokens, command_class = Code_line.split(execute_args.code_line)

            execute_args.arguments = self.__tokens_to_arguments(line_tokens)
            execute_args.code_lines = code_lines
            execute_args.code_index = execution_context[Context._CODE_INDEX]

            with PrefaceLogger(self._code.get_code_line_description(execution_context[Context._CODE_NAME], line_number), self.logger):
                command_class.execute(execute_args)

            execution_context[Context._CODE_INDEX] += 1
            
        #popping code context from code stack
        self._execution_stack.pop()
        #if function call var stack is popped
        if execution_context[Context._CODE_IS_FUNCTION]:
            self._variable_stack.pop()

    def jump_to_code(self, new_code_index):
        self._execution_stack[-1][Context._CODE_INDEX] = new_code_index - 1 # - 1 is due to #call_context[Context._CODE_INDEX] += 1 in execute_code loop!!!

################################################################################
    def push_call_tokens(self, call_tokens):
        self._call_tokens = call_tokens

    def pop_call_tokens(self):
        ret = self._call_tokens
        self._call_tokens = None
        return ret

    def exit(self):
        self._exit = True

################################################################################
    def return_execute_code(self, value = None):
        code_lines = self._code.get_code_lines(self._execution_stack[-1][Context._CODE_NAME])
        self.jump_to_code(len(code_lines))
        self._return = value

    def get_return_value(self):
        return self._return

################################################################################
    def run(self):
        self.execute_code(self._code.main_code_name())

    def run_from_restored_context(self):
        if len(self._execution_stack) == 0:
            self.execute_code(self._code.main_code_name())
        else:
            self.execute_code(None, 0)

################################################################################
    def to_json_dict(self):
        return {'execution_stack':deepcopy(self._execution_stack),
                'variable_stack':deepcopy(self._variable_stack)}

    def from_json_dict(self, json_dict):
        self._execution_stack = json_dict['execution_stack']
        self._variable_stack = json_dict['variable_stack']

################################################################################
    def store_context(self, file_name):
        ''' Store entire context with code into file 'file_name'.
If file_name is None, file_name is taken from code, '.bin' extension is added and folder is the same as code '''
        if file_name == None:
            file_name = os.path.join(self._code._code_path, self._code.main_code_name() + '.bin')

        json_dict = {'code':self._code.to_json_dict(),
                     'context':self.to_json_dict()}

        j = json.dumps(json_dict, indent=2)
        with open(file_name, 'w') as f:
            f.write(j)

    def restore_context(self, file_name):
        if file_name == None:
            return

        with open(file_name) as f:
            json_dict = json.load(f)

        self._code.from_json_dict(json_dict['code'], self._logger)
        self.from_json_dict(json_dict['context'])

################################################################################

