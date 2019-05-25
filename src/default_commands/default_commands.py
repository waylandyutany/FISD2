from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME

################################################################################
@command_class("set")
@tokenizer_class("set")
class SetCommand(Command):
    @classmethod
    def parse(cls):
        print("SetCommand.parse()")

    @classmethod
    def execute(cls):
        print("SetCommand.execute()")

    @classmethod
    def tokenize(cls, tokens):
        if tokens.type(0) == TOKEN_NAME and tokens.value(1) == '=':
            tokens.insert_token(0, TOKEN_NAME, 'set')


