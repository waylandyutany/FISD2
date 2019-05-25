from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME

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
        if (len(tokens) > 1) and (tokens[0]['id'] == TOKEN_NAME) and (tokens[1]['val'] == '='):
            tokens.insert(0,{'id':TOKEN_NAME, 'val':'set'})
        return tokens
