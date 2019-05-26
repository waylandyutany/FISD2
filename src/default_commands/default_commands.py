from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME
from core.logger import Logger

################################################################################
# SET Command
################################################################################
@command_class("set")
@tokenizer_class("set")
class SetCommand(Command):
    @classmethod
    def parse(cls):
        Logger.log.info("SetCommand.parse()")

    @classmethod
    def execute(cls, context, arguments):
        Logger.log.info("SetCommand.execute()")

    @classmethod
    def tokenize(cls, tokens):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '='):
            tokens.insert_token(0, TOKEN_NAME, 'set')

################################################################################
# PRINT Command
################################################################################
@command_class("print")
class PrintCommand(Command):
    @classmethod
    def parse(cls):
        Logger.log.info("PrintCommand.parse()")

    @classmethod
    def execute(cls, context, arguments):
        Logger.log.info("PrintCommand.execute()")

################################################################################
# EXECUTE Command
################################################################################
@command_class("execute")
class PrintCommand(Command):
    @classmethod
    def parse(cls):
        Logger.log.info("ExecuteCommand.parse()")

    @classmethod
    def execute(cls, context, arguments):
        Logger.log.info("ExecuteCommand.execute()")

