from core.code import Code
from copy import deepcopy
from core.code_line import Code_line
from core.utils import PrefaceLogger
from core.variable_stack import Variable_stack
from core.execution_stack import Execution_stack

import json, os

from default_commands.fisd_commands import Fisd_restore_context_command #@todo remove this dependency
import core.core as core

################################################################################
class ExecuteArgs: 
    def __init__(self, _context, _logger, _code_name, _code_lines):
        self.code_name = _code_name
        self.code_lines = _code_lines
        self.code_index = None
        self.code_line = None

        self.arguments = None

        self.context = _context
        self.logger = _logger

################################################################################
class Context:
    _variable_case_sensitive = False

    def __init__(self, code, logger):
        self._code = code

        self._call_tokens = None
        self._return = None
        self._exit = False

        self._logger = logger

        self._execution_stack = []
        self._variable_stack = Variable_stack(Context._variable_case_sensitive)

################################################################################
    def to_json_dict(self):
        return {'execution_stack':deepcopy(self._execution_stack),
                'variable_stack':self._variable_stack.to_json_dict()}

    def from_json_dict(self, json_dict):
        self._execution_stack = json_dict['execution_stack']
        self._variable_stack.from_json_dict(json_dict['variable_stack'])

################################################################################
    def get_variable(self, name):
        return self._variable_stack.get_variable(name)

    def set_variable(self, name, value):
        self._variable_stack.set_variable(name, value)

################################################################################
    def __push_execution_context(self, code_name):
        #creating code execution context
        execution_context = {Execution_stack._CODE_NAME:code_name,
                                Execution_stack._CODE_INDEX:0,
                                Execution_stack._CODE_IS_FUNCTION:self._code.is_code_function(code_name)}
        #pushing code context to the stack
        self._execution_stack.append(execution_context)
        #if function call new var stack is pushed
        if execution_context[Execution_stack._CODE_IS_FUNCTION]:
            self._variable_stack.push()

        return execution_context

    def __restore_execution_context(self, execution_stack_index):
        execution_context = self._execution_stack[execution_stack_index]
        if execution_stack_index + 1 < len(self._execution_stack):
            self.execute_code(execution_context[Execution_stack._CODE_NAME], execution_stack_index + 1)
        else:# in case of last execution context, we search for restoration point code line
                # so code will start from that point
            code_lines = self._code.get_code_lines(execution_context[Execution_stack._CODE_NAME])
            while execution_context[Execution_stack._CODE_INDEX] < len(code_lines):
                cmd_class = Code_line.get_command_class(code_lines[execution_context[Execution_stack._CODE_INDEX]])
                if cmd_class._keyword == Fisd_restore_context_command._keyword:
                    break
                execution_context[Execution_stack._CODE_INDEX] += 1

        # after restoring always starts from next code line
        execution_context[Execution_stack._CODE_INDEX] += 1

        return execution_context

################################################################################
    def execute_code(self, code_name, execution_stack_index = None):
        execution_context = self.__push_execution_context(code_name) if execution_stack_index == None else\
                            self.__restore_execution_context(execution_stack_index)

        #getting code lines from the code
        code_lines = self._code.get_code_lines(execution_context[Execution_stack._CODE_NAME])
        execute_args = ExecuteArgs(self, self._logger, execution_context[Execution_stack._CODE_NAME], code_lines)

        #executing commands
        while execution_context[Execution_stack._CODE_INDEX] < len(code_lines) and (self._exit == False):
            execute_args.code_line = code_lines[execution_context[Execution_stack._CODE_INDEX]]

            line_number, line_tokens, command_class = Code_line.split(execute_args.code_line)

            execute_args.arguments = self._variable_stack.tokens_to_arguments(line_tokens)
            execute_args.code_lines = code_lines
            execute_args.code_index = execution_context[Execution_stack._CODE_INDEX]

            with PrefaceLogger(self._code.get_code_line_description(execution_context[Execution_stack._CODE_NAME], line_number), self._logger):
                command_class.execute(execute_args)

            execution_context[Execution_stack._CODE_INDEX] += 1
            
        #popping code context from code stack
        self._execution_stack.pop()
        #if function call var stack is popped
        if execution_context[Execution_stack._CODE_IS_FUNCTION]:
            self._variable_stack.pop()

    def jump_to_code(self, new_code_index):
        self._execution_stack[-1][Execution_stack._CODE_INDEX] = new_code_index - 1 # - 1 is due to #call_context[Context._CODE_INDEX] += 1 in execute_code loop!!!

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
        code_lines = self._code.get_code_lines(self._execution_stack[-1][Execution_stack._CODE_NAME])
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
    def store_context(self, file_name):
        ''' Store entire context with code into file 'file_name'.
If file_name is None, file_name is taken from code, '.bin' extension is added and folder is the same as code '''
        if file_name == None:
            file_name = self._code.main_code_name() + core.__binary_fisd_file_extension__

        json_dict = {'code':self._code.to_json_dict(),
                     'context':self.to_json_dict()}

        j = json.dumps(json_dict, indent=2)
        with open(file_name, 'w') as f:
            f.write(j)

    def restore_context(self, file_name):
        with open(file_name) as f:
            json_dict = json.load(f)

        self._code.from_json_dict(json_dict['code'], self._logger)
        self.from_json_dict(json_dict['context'])

################################################################################

