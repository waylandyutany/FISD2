from core.execution_stack import Execution_stack
from core.code_line import Code_line
from core.tokens import Tokens
from copy import deepcopy

################################################################################
class Arguments:
    def __init__(self):
        self.__args = []

    def __str__(self):
        return str(self.__args)

    def __len__(self):
        return len(self.__args)

    def add(self, name, value):
        self.__args.append((name, value))

    def value(self, index):
        try:return self.__args[index][1]
        except:return None

    def name(self, index):
        try:return self.__args[index][0]
        except:return None

    def copy(self):
        return deepcopy(self)

################################################################################
class Execution_args: 
    def __init__(self, context, code, logger):
        self.__context = context
        self.__code = code
        self.__logger = logger

        self.__arguments = context._variable_stack.tokens_to_arguments(Code_line.get_line_tokens(self.code_line))

        self.__args = Arguments()

        arg_tokens = Tokens(deepcopy(self.__arguments.tokens()))
        left_bracket_index = arg_tokens.find_op('(')
        if left_bracket_index != None:
            arguments = arg_tokens.pop_tokens(left_bracket_index,len(arg_tokens) - 1).split_tokens_by_op(',')
            for argument in arguments:
                if not argument.empty():
                    argument_name = None
                    if argument.is_keyword(0):
                        argument_name = argument.value(0)
                        argument.pop_tokens(-1, 1)
                    try:
                        argument_value = argument.evaluate()
                        self.__args.add(argument_name, argument_value)
                    except:
                        self.__args.add(argument_name, None)

    @property
    def args(self):
        return self.__args

################################################################################

    def __str__(self):
        return str(self.__args)

################################################################################
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
