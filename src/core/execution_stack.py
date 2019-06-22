from default_commands.fisd_commands import Fisd_restore_context_command #@todo remove this dependency

from copy import deepcopy
from core.code_line import Code_line

import os

################################################################################
class Execution_stack:
    _CODE_NAME = 'code_name'
    _CODE_INDEX = 'code_index'
    _CODE_IS_FUNCTION = 'is_function'

    def __init__(self, code, variable_stack):
        self._code = code
        self._variable_stack = variable_stack
        self._stack = []

################################################################################
    def push_execution_context(self, code_name):
        #creating code execution context
        execution_context = {Execution_stack._CODE_NAME:code_name,
                                Execution_stack._CODE_INDEX:0,
                                Execution_stack._CODE_IS_FUNCTION:self._code.is_code_function(code_name)}
        #pushing code context to the stack
        self._stack.append(execution_context)
        #if function call new var stack is pushed
        if execution_context[Execution_stack._CODE_IS_FUNCTION]:
            self._variable_stack.push()

        return execution_context

    def restore_execution_context(self, execution_stack_index, context):
        execution_context = self._stack[execution_stack_index]
        if execution_stack_index + 1 < len(self._stack):
            context.execute_code(execution_context[Execution_stack._CODE_NAME], execution_stack_index + 1)
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

    def pop(self):
        self._stack.pop()

    def is_empty(self):
        return len(self._stack) == 0

################################################################################
    def to_json_dict(self):
        return {'stack':deepcopy(self._stack)}

    def from_json_dict(self, json_dict):
        self._stack = json_dict['stack']
        
################################################################################
    def jump_to_code(self, new_code_index):
        self._stack[-1][Execution_stack._CODE_INDEX] = new_code_index - 1 # - 1 is due to #call_context[Context._CODE_INDEX] += 1 in execute_code loop!!!

################################################################################
    def current_code_name(self):
        return self._stack[-1][Execution_stack._CODE_NAME]

    #@todo in case of function we must take path from FUNCTION_FILE_NAME !!!
    def __current_code_path(self):
        return self._stack[-1][Execution_stack._CODE_NAME]

    def current_file_name(self):
        return os.path.basename(self.__current_code_path(self))

    def current_file_folder(self):
        file_path, file_name = os.path.split(self.__current_code_path(self))
        _, file_folder = os.path.split(file_path)
        return file_folder

################################################################################
