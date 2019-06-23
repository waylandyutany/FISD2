from core.code_line import Code_line
from core.tokens import Tokens
from core.commands import command_class, Command, Commands
from default_commands.procedure_commands import CallCommand

################################################################################
# SETRET Command
################################################################################
@command_class()
class SetretCommand(Command):
    _keyword = 'setret'

    @staticmethod
    def parse(pargs):
        pass    

    @staticmethod
    def execute(eargs):
        eargs.context.set_variable(eargs.arguments.value(1), eargs.context.get_return_value())

    @staticmethod
    def create_code_line(line_number, var_name):
        tokens = Tokens("{}".format(SetretCommand._keyword))
        tokens.insert_name(1, var_name)
        tokens.mark_as_keyword(0)
        tokens.mark_as_keyword(1)
        code_line = Code_line.create(line_number, tokens, SetretCommand)
        return code_line

################################################################################
# Code_evaluation
################################################################################
class Code_evaluation:
    _FISD_FUNCTION = 0
    _FISD_COMMAND = 1
    #@todo error when function name == variable name
    @classmethod
    def rightest_function(cls, tokens, code):
        ret = None
        for i in range(0, len(tokens) - 2):
            if tokens.is_keyword(i) and tokens.is_op(i + 1) and tokens.is_value(i + 1, '('):
                nested_counter = 0
                for j in range(i + 2, len(tokens)):
                    if tokens.is_op(j):
                        if tokens.is_value(j, '('):
                            nested_counter += 1
                        elif tokens.is_value(j, ')'):
                            if nested_counter == 0:
                                # only our fisd functions are accepted
                                if code.get_code_lines(tokens.value(i)):
                                    ret = (i, j, cls._FISD_FUNCTION)
                                elif Commands.find_command(tokens.value(i)) != None:
                                    ret = (i, j, cls._FISD_COMMAND)
                                break
                            else:
                                nested_counter -= 1
        return ret

    @staticmethod
    def mark_functions_as_keywords(tokens):
        for i in range(0, len(tokens) - 2):
            if tokens.is_name(i) and tokens.is_op(i + 1) and tokens.is_value(i + 1, '('):
                tokens.mark_as_keyword(i)

    @classmethod
    def evaluate_function_calls(cls, pargs):
        line_tokens = Code_line.get_line_tokens(pargs.code_line)
        line_number = Code_line.get_line_number(pargs.code_line)
        cls.mark_functions_as_keywords(line_tokens)
        rightest_function = cls.rightest_function(line_tokens, pargs.code)#@ can be done via generator and ienumerate to get the var_index
        var_index = 0
        while rightest_function:
            # add # before set_ret_{} variable name to prevent collision with other 'normal' variables
            var_name = "#setret_{}".format(var_index)

            i, j, type = rightest_function
            function_tokens = line_tokens.pop_tokens(i - 1, j + 1)
            func_name = function_tokens.value(0)
            line_tokens.insert_name(i, var_name)

            if type == cls._FISD_FUNCTION:
                call_code_line = CallCommand.create_code_line(line_number, function_tokens)
            elif type == cls._FISD_COMMAND:
                call_code_line = Commands.find_command(func_name).create_code_line(line_number, function_tokens)

            call_ret_code_line = SetretCommand.create_code_line(line_number, var_name)

            pargs.code_lines_insertion.insert_before(line_number, call_code_line)
            pargs.code_lines_insertion.insert_before(line_number, call_ret_code_line)

            rightest_function = cls.rightest_function(line_tokens, pargs.code)
            var_index += 1
