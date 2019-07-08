from core.code.code import Code
from core.code.code_line import Code_line
from core.execution.variable_stack import Variable_stack
from core.execution.execution import Execution
from core.execution.execution_stack import Execution_stack
from core.execution.execution_params import ExecutionParams

from core.safe_utils import safe_path
from core.utils import PrefaceLogger

import core.core as core
import json

################################################################################
class Context:
    def __init__(self, code, logger):
        self._code = code

        self._call_tokens = None
        self._return = None
        self._exit = False

        self._logger = logger

        self._variable_stack = Variable_stack(core.__variable_case_sensitive__)
        self._execution = Execution(self._code, self._variable_stack)

################################################################################
    @property
    def execution(self):
        return self._execution

################################################################################
    def to_json_dict(self):
        return {'execution_stack':self._execution.to_json_dict(),
                'variable_stack':self._variable_stack.to_json_dict(),
                'return':self._return}

    def from_json_dict(self, json_dict):
        self._execution.from_json_dict(json_dict['execution_stack'])
        self._variable_stack.from_json_dict(json_dict['variable_stack'])
        self._return = json_dict['return']

################################################################################
    def get_variable(self, name):
        return self._variable_stack.get_variable(name)

    def set_variable(self, name, value):
        self._variable_stack.set_variable(name, value)

################################################################################
    def execute_code(self, code_name, execution_stack_index = None):
        execution_context = self._execution.push_execution_context(code_name) if execution_stack_index == None else\
                            self._execution.restore_execution_context(execution_stack_index, self)

        #getting code lines from the code
        code_lines = self._code.get_code_lines(execution_context[Execution_stack._CODE_NAME])

        #executing commands
        while execution_context[Execution_stack._CODE_INDEX] < len(code_lines) and (self._exit == False):
            execution_params = ExecutionParams(self, self._code, self._logger)

            with PrefaceLogger(self._code.get_code_line_description(execution_params.code_name, execution_params.line_number), self._logger):
                execution_params.command_class.execute(execution_params)

            execution_context[Execution_stack._CODE_INDEX] += 1
            
        #popping code context from code stack
        self._execution.pop_execution()

    def jump_to_code(self, new_code_index):
        self._execution.jump_to_code(new_code_index)

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
        code_lines = self._code.get_code_lines(self._execution.current_code_name)
        self.jump_to_code(len(code_lines))
        self._return = value

    def get_return_value(self):
        return self._return

    def set_return_value(self, value):
        self._return = value
################################################################################
    def run(self):
        self.execute_code(self._code.main_code_name())

    def run_from_restored_context(self):
        if self._execution.is_empty:
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
        with open(safe_path(file_name), 'w') as f:
            f.write(j)

    def restore_context(self, file_name):
        with open(file_name) as f:
            json_dict = json.load(f)

        self._code.from_json_dict(json_dict['code'], self._logger)
        self.from_json_dict(json_dict['context'])

################################################################################

