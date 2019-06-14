from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME, Tokens
from core.code_line import Code_line

from default_commands.procedure_commands import CallCommand

################################################################################
# JUMP Command
################################################################################
@command_class()
class JumpCommand(Command):
    _JUMP = 'jump'
    _keyword = _JUMP

    @staticmethod
    def parse(pargs):
        pass    

    @staticmethod
    def execute(eargs):
        eargs.context.jump_to_code(Code_line.get_jump(eargs.code_line, JumpCommand._keyword))

    @staticmethod
    def create_code_line(line_number, jump_label_name):
        tokens = Tokens(JumpCommand._keyword)
        tokens.mark_as_keyword(0)
        code_line = Code_line.create(line_number, tokens, JumpCommand)
        Code_line.add_jump(code_line, JumpCommand._keyword, jump_label_name)
        return code_line

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
        tokens = Tokens("{} {}".format(SetretCommand._keyword, var_name))
        tokens.mark_as_keyword(0)
        tokens.mark_as_keyword(1)
        code_line = Code_line.create(line_number, tokens, SetretCommand)
        return code_line
        
################################################################################
# SET Command
################################################################################
@command_class()
@tokenizer_class()
class SetCommand(Command):
    _keyword = 'set'

    #@todo error when function name == variable name
    @staticmethod
    def rightest_function(tokens, code):
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
                                    ret = (i,j)
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
    def parse(cls, pargs):
        line_tokens = Code_line.get_line_tokens(pargs.code_line)
        line_number = Code_line.get_line_number(pargs.code_line)

        cls.mark_functions_as_keywords(line_tokens)
        rightest_function = cls.rightest_function(line_tokens, pargs.code)
        var_index = 0
        while rightest_function:
            #@todo take a look on double set_ret0 in line_tokens !!!
            #@todo handle already existing varn_name !!!
            var_name = "setret_{}".format(var_index)
            i, j = rightest_function
            function_tokens = line_tokens.pop_tokens(i - 1, j + 1)
            line_tokens.insert_name(i, var_name)
            #pargs.logger.info(str(function_tokens))

            call_code_line = CallCommand.create_code_line(line_number, function_tokens)
            call_ret_code_line = SetretCommand.create_code_line(line_number, var_name)

            pargs.code_lines_insertion.insert_before(line_number, call_code_line)
            pargs.code_lines_insertion.insert_before(line_number, call_ret_code_line)

            rightest_function = cls.rightest_function(line_tokens, pargs.code)
            var_index += 1

        line_tokens.mark_as_keyword(1)

    @staticmethod
    def execute(eargs):
        variable_name = eargs.arguments.value(1)
        try:
            evaluated_value = eargs.arguments.evaluate_tokens(2, len(eargs.arguments))
        except Exception as e:
            eargs.logger.error("Exception during '{}' evaluation! {}!".format(variable_name, e))
            return

        #context.logger.debug("'{}' evaluated '{} = {}'".format(variable_name, string_to_evaluate, evaluated_value))

        eargs.context.set_variable(variable_name, evaluated_value)

    @staticmethod
    def tokenize(tokens, logger):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '='):
            tokens.insert_name(0, SetCommand._keyword)

################################################################################
# PRINT Command
################################################################################
@command_class()
class PrintCommand(Command):
    _keyword = 'print'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("PRINT {}".format("".join( ( str(eargs.arguments.value_str(i)) for i in range(1, len(eargs.arguments)) ) )))

################################################################################
# EXECUTE Command
################################################################################
@command_class()
class ExecuteCommand(Command):
    _keyword = 'execute'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.context.execute_code(eargs.arguments.value_str(1))

