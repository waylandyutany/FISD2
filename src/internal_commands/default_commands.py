from core.commands import command_class, Command
from core.command_type import CallableCommand as Callable
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
    def execute(params):
        params.context.jump_to_code(Code_line.get_jump(params.code_line, JumpCommand._keyword))

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
    def execute(params):
        variable_name = params.raw_args.value(1)
        try:
            evaluated_value = params.raw_args.evaluate_tokens(2, len(params.raw_args))
        except Exception as e:
            params.logger.error("Exception during '{}' evaluation! {}!".format(variable_name, e))
            return

        params.context.set_variable(variable_name, evaluated_value)

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
    def execute(cls, params):
        params.logger.info("PRINT {}".format("".join( ( str(params.raw_args.value_str(i)) for i in range(1, len(params.raw_args)) ) )))

################################################################################
# EXECUTE Command
################################################################################
@command_class('execute')
class ExecuteCommand(Command):
    @classmethod
    def execute(cls, params):
        params.context.execute_code(params.raw_args.value_str(1))

################################################################################
# EXIT Command
################################################################################
@command_class('exit')
class ExitCommand(Command):
    @classmethod
    def execute(cls, params):
        params.context.exit()

################################################################################
# WAIT_TO_SECONDS Command
################################################################################
@command_class('time_to_seconds', Callable())
class Time_to_secondsCommand(Command):
    @staticmethod
    def string_to_seconds(s):
        float_part = 0.0
        time_and_float = s.split(".")
        try:float_part = float("0." + time_and_float[1])
        except:pass
        time_part = time_and_float[0].split(":")
        if len(time_part) == 3:
            return (int(time_part[0]) * 3600) + (int(time_part[1]) * 60) + int(time_part[0]) + float_part
        elif len(time_part) == 2:
            return (int(time_part[0]) * 60) + int(time_part[1]) + float_part
        elif len(time_part) == 1:
            return int(time_part[0]) + float_part
        return float_part

    @classmethod
    def time_to_seconds(cls, params):
        eargs = params.evaluated_args
        if len(eargs) == 3:
            return((eargs.value(0) * 3600) + (eargs.value(1) * 60) + eargs.value(2))
        elif len(eargs) == 2:
            return((eargs.value(0) * 60) + eargs.value(1))
        else:
            if eargs.type(0) == str:
                return(cls.string_to_seconds(eargs.value(0)))
            else:
                return(eargs.value(0))

    @classmethod
    def execute(cls, params):
        params.set_return(cls.time_to_seconds(params))

################################################################################
# WAIT Command
################################################################################
@command_class('wait', Callable())
class WaitCommand(Command):
    @classmethod
    def execute(cls, params):
        time_to_seconds = Time_to_secondsCommand.time_to_seconds(params)
        params.logger.info("Waiting '{}'s...".format(time_to_seconds))

################################################################################
# DATE Command
################################################################################
@command_class('date')
class DateCommand(Command):
    @classmethod
    def execute(cls, params):
        params.set_return(datetime.datetime.now().strftime("%Y-%m-%d"))

################################################################################
# TIME Command
################################################################################
@command_class('time')
class TimeCommand(Command):
    @classmethod
    def execute(cls, params):
        params.set_return(datetime.datetime.now().strftime("%H:%M:%S"))

