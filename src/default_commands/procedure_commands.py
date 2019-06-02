from core.commands import command_class, Command
from default_commands.keywords import Keywords
from core.tokens import tokenizer_class, TOKEN_NAME, TOKEN_OP

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
        pass

    @classmethod
    def tokenize(cls, tokens, logger):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '('):
            tokens.insert_name(0, Keywords._CALL)
