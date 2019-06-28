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
        variable_name = eargs.raw_args.value(1)
        try:
            evaluated_value = eargs.raw_args.evaluate_tokens(2, len(eargs.raw_args))
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
@command_class('print')
class PrintCommand(Command):
    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("PRINT {}".format("".join( ( str(eargs.raw_args.value_str(i)) for i in range(1, len(eargs.raw_args)) ) )))

################################################################################
# EXECUTE Command
################################################################################
@command_class('execute')
class ExecuteCommand(Command):
    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.context.execute_code(eargs.raw_args.value_str(1))

################################################################################
# EXIT Command
################################################################################
@command_class('exit')
class ExitCommand(Command):
    @classmethod
    def execute(cls, eargs):
        eargs.context.exit()

################################################################################
# WAIT Command
################################################################################
@command_class('wait')
class WaitCommand(Command):
    """
    Valid formats
    """
    _wait_formats = ["%H:%M:%S.%f", "%H:%M:%S", "%M:%S.%f", "%M:%S", "%S.%f", "%S"]

    @classmethod
    def get_time(cls, string):
        for wait_format in cls._wait_formats:
            try:return datetime.datetime.strptime(string, wait_format)
            except:continue
        return None

    @classmethod
    def execute(cls, eargs):
        wait_string = eargs.raw_args.sub_tokens(0, len(eargs.raw_args)).to_string("")
        tm = cls.get_time(wait_string)
        if tm:
            wait_in_s = (tm.hour*3600) + (tm.minute*60) + tm.second + (tm.microsecond / 1000000.0)
            eargs.logger.info(wait_string + "->" + str(tm) + "->" + str(wait_in_s) + "s")
        else:
            eargs.logger.info(wait_string)

################################################################################
# DATE Command
################################################################################
@command_class('date')
class DateCommand(Command):
    @classmethod
    def execute(cls, eargs):
        eargs.set_return(datetime.datetime.now().strftime("%Y-%m-%d"))

################################################################################
# TIME Command
################################################################################
@command_class('time')
class TimeCommand(Command):
    @classmethod
    def execute(cls, eargs):
        eargs.set_return(datetime.datetime.now().strftime("%H:%M:%S"))

