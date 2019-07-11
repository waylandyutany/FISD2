from core.execution.execution_stack import Execution_stack
from core.execution.evaluated_arguments import EvaluatedArguments
from core.execution.raw_arguments import RawArguments
from core.code.code_line import Code_line

################################################################################
class ExecutionParams: 
    def __init__(self, context, code, logger):
        self.__context = context
        self.__code = code
        self.__logger = logger

        self.__raw_args = RawArguments(context._variable_stack, self.line_tokens)
        self.__evaluated_args = EvaluatedArguments(self.__raw_args)

    @property
    def evaluated_args(self):
        return self.__evaluated_args

    @property
    def raw_args(self):
        return self.__raw_args

################################################################################
    def set_return(self, value):
        self.context.set_return_value(value)

################################################################################
    def __str__(self):
        return str(self.__evaluated_args)

################################################################################
    @property
    def code_name(self):
        return self.__context._execution.current_code_name

    @property
    def code_lines(self):
        return self.__code.get_code_lines(self.code_name)

    @property
    def code_index(self):
        return self.__context._execution.current_code_index

    @property
    def code_line(self):
        return self.code_lines[self.code_index]

    @property
    def line_number(self):
        return self.__context._execution.current_line_number

    @property
    def command_class(self):
        return Code_line.get_command_class(self.code_line)

    @property
    def line_tokens(self):
        return Code_line.get_line_tokens(self.code_line)

    @property
    def context(self):
        return self.__context

    @property
    def code(self):
        return self.__code

    @property
    def logger(self):
        return self.__logger
