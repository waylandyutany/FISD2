from core.commands import command_class, Command
from core.code import tokenizer, NAME, OP

@command_class("set")
class SetCommand(Command):
    @classmethod
    def parse(cls):
        print("SetCommand.parse()")

    @classmethod
    def execute(cls):
        print("SetCommand.execute()")

@tokenizer("set")
def set_tokenizer(tokens):
    if (len(tokens) > 1) and (tokens[0]['id'] == NAME) and (tokens[1]['val'] == '='):
        tokens.insert(0,{'id':NAME, 'val':'set'})
    return tokens
