from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME, TOKEN_OP

################################################################################
# PROC Command
################################################################################
@command_class()
class ProcCommand(Command):
    _PROC = 'proc'
    _keyword = _PROC

    @staticmethod
    def parse(parse_args):
        pass

    @staticmethod
    def execute(execute_args):
        pass

################################################################################
# END_PROC Command
################################################################################
@command_class()
class EndProcCommand(Command):
    _END_PROC = 'endproc'
    _keyword = _END_PROC

    @staticmethod
    def parse(parse_args):
        pass

    @staticmethod
    def execute(execute_args):
        pass

################################################################################
# RETURN Command
################################################################################
@command_class()
class ReturnCommand(Command):
    _RETURN = 'return'
    _keyword = _RETURN

    @staticmethod
    def parse(parse_args):
        pass

    @staticmethod
    def execute(execute_args):
        pass

################################################################################
# CALL Command
################################################################################
@command_class()
@tokenizer_class()
class CallCommand(Command):
    _CALL = 'call'
    _keyword = _CALL

    @staticmethod
    def parse(parse_args):
        pass

    @staticmethod
    def execute(execute_args):
        execute_args.context.execute_code(execute_args.arguments.value_str(1))

    @staticmethod
    def tokenize(tokens, logger):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '('):
            tokens.insert_name(0, CallCommand._keyword)
