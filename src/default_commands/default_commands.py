from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME
from core.logger import Logger

################################################################################
@command_class("set")
@tokenizer_class("set")
class SetCommand(Command):
    @classmethod
    def parse(cls):
        Logger.log.info("SetCommand.parse()")

    @classmethod
    def execute(cls):
        Logger.log.info("SetCommand.execute()")

    @classmethod
    def tokenize(cls, tokens):
        if tokens.is_name(0) and tokens.is_value(1, '='):
            tokens.insert_token(0, TOKEN_NAME, 'set')


