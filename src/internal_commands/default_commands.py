from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME, Tokens
from core.code_line import Code_line
import datetime

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
# SET Command
################################################################################
@command_class()
@tokenizer_class()
class SetCommand(Command):
    _keyword = 'set'

    @classmethod
    def parse(cls, pargs):
        line_tokens = Code_line.get_line_tokens(pargs.code_line)
        line_tokens.mark_as_keyword(1)

    @staticmethod
    def execute(eargs):
        variable_name = eargs.arguments.value(1)
        try:
            evaluated_value = eargs.arguments.evaluate_tokens(2, len(eargs.arguments))
        except Exception as e:
            eargs.logger.error("Exception during '{}' evaluation! {}!".format(variable_name, e))
            return

        eargs.context.set_variable(variable_name, evaluated_value)

    @classmethod
    def tokenize_op_op(cls, tokens, logger, op):
        if tokens.is_op_value(1, op) and tokens.is_op_value(2, op):
            tokens.init_from_string("{0} {1} = {1} {2} 1".format(SetCommand._keyword, tokens.value(0), op))

    @classmethod
    def tokenize_op_eq(cls, tokens, logger, op):
        if tokens.is_op_value(1, op + "="):
            post_tokens_string = tokens.sub_tokens(1, len(tokens)).to_string()
            tokens.init_from_string("{0} {1} = {1} {2} {3}".format(SetCommand._keyword, tokens.value(0), op, post_tokens_string))

    @classmethod
    def tokenize(cls, tokens, logger):
        if tokens.is_name(0):
            cls.tokenize_op_op(tokens, logger, '+') #value++
            cls.tokenize_op_op(tokens, logger, '-') #value--

            cls.tokenize_op_eq(tokens, logger, '+') #value += ...
            cls.tokenize_op_eq(tokens, logger, '-') #value -= ...
            cls.tokenize_op_eq(tokens, logger, '*') #value *= ...
            cls.tokenize_op_eq(tokens, logger, '/') #value /= ...
            cls.tokenize_op_eq(tokens, logger, '%') #value /= ...

            if tokens.is_op_value(1, '='):
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

################################################################################
# EXIT Command
################################################################################
@command_class()
class ExitCommand(Command):
    _keyword = 'exit'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.context.exit()

################################################################################
# WAIT Command
################################################################################
@command_class()
class WaitCommand(Command):
    _keyword = 'wait'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.error("Not implemented yet!")

################################################################################
# DATE Command
################################################################################
@command_class()
class DateCommand(Command):
    _keyword = 'date'

    @classmethod
    def execute(cls, eargs):
        eargs.set_return(datetime.datetime.now().strftime("%Y-%m-%d"))

################################################################################
# TIME Command
################################################################################
@command_class()
class TimeCommand(Command):
    _keyword = 'time'

    @classmethod
    def execute(cls, eargs):
        eargs.set_return(datetime.datetime.now().strftime("%H:%M:%S"))

