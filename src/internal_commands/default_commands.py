from core.commands import command_class, Command
from core.command_type import CallableCommand as Callable
from core.tokens import tokenizer_class, TOKEN_NAME, Tokens
from core.code_line import Code_line

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
