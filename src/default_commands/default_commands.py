from core.commands import command_class, Command

@command_class("set")
class SetCommand(Command):
    @classmethod
    def parse(cls):
        print("SetCommand.parse()")

    @classmethod
    def execute(cls):
        print("SetCommand.execute()")
