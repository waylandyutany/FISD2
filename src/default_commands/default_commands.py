from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME
from core.logger import Logger
from default_commands.keywords import Keywords

################################################################################
# SET Command
################################################################################
@command_class(Keywords._SET)
@tokenizer_class(Keywords._SET)
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
            tokens.insert_name(0, 'set')

################################################################################
# PRINT Command
################################################################################
@command_class(Keywords._PRINT)
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
@command_class(Keywords._EXECUTE)
class PrintCommand(Command):
    @classmethod
    def parse(cls):
        Logger.log.info("ExecuteCommand.parse()")

    @classmethod
    def execute(cls, context, arguments):
        Logger.log.info("ExecuteCommand.execute()")

