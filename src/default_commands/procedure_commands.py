from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME, TOKEN_OP

################################################################################
# Keywords
################################################################################
class Keywords:
    _PROC = 'proc'
    _END_PROC = 'endproc'
    _RETURN = 'return'
    _CALL = 'call'

################################################################################
# PROC Command
################################################################################
@command_class(Keywords._PROC)
class ProcCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        pass

################################################################################
# END_PROC Command
################################################################################
@command_class(Keywords._END_PROC)
class EndProcCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        pass

################################################################################
# RETURN Command
################################################################################
@command_class(Keywords._RETURN)
class ReturnCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        pass

################################################################################
# CALL Command
################################################################################
@command_class(Keywords._CALL)
@tokenizer_class(Keywords._CALL)
class CallCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        execute_args.context.execute_code(execute_args.arguments.value_str(1))

    @classmethod
    def tokenize(cls, tokens, logger):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '('):
            tokens.insert_name(0, Keywords._CALL)
