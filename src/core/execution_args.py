from core.execution_stack import Execution_stack
from core.code_line import Code_line

################################################################################
class Execution_args: 
    def __init__(self, context, code, logger):
        self.__context = context
        self.__code = code
        self.__logger = logger

        self.__arguments = context._variable_stack.tokens_to_arguments(Code_line.get_line_tokens(self.code_line))

    def __str__(self):
        return str(self.__arguments)

    @property
    def code_name(self):
        return self.__context._execution.current_code_name()

    @property
    def code_lines(self):
        return self.__code.get_code_lines(self.code_name)

    @property
    def code_index(self):
        return self.__context._execution.current_code_index()

    @property
    def code_line(self):
        return self.code_lines[self.code_index]

    @property
    def line_number(self):
        return self.__context._execution.current_line_number()

    @property
    def command_class(self):
        return Code_line.get_command_class(self.code_line)

    @property
    def context(self):
        return self.__context

    #@property
    #def code(self):
    #    return self.__code

    @property
    def logger(self):
        return self.__logger

    @property
    def arguments(self):
        return self.__arguments
