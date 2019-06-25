from core.execution_stack import Execution_stack
from core.code_line import Code_line
from core.tokens import Tokens
from copy import deepcopy

################################################################################
class Execution_args: 
    def __init__(self, context, code, logger):
        self.__context = context
        self.__code = code
        self.__logger = logger

        self.__arguments = context._variable_stack.tokens_to_arguments(Code_line.get_line_tokens(self.code_line))

        self._arg_tokens = Tokens(deepcopy(self.__arguments.tokens()))

        #removing command name
        self._arg_tokens.pop_tokens(-1,1)

        self.__args = []

        #removing '(' from the beginning
        if self._arg_tokens.is_op(0) and self._arg_tokens.is_value(0,'(') and self._arg_tokens.is_op(-1) and self._arg_tokens.is_value(-1,')'):
            arguments = self._arg_tokens.pop_tokens(0,len(self._arg_tokens) - 1).split_tokens_by_op(',')
            for argument in arguments:
                if not argument.empty():
                    argument_value = argument.evaluate()
                    self.__args.append(argument_value)
                else:
                    self.__args.append(None)

    def __str__(self):
        return str(self.__args)

    def argument(self, index):
        try:
            return self.__args[index]
        except:
            pass
        return None

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
