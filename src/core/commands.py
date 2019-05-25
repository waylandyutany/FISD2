################################################################################
class Command:
    @staticmethod
    def parse():
        print("Command.parse()")

    @staticmethod
    def execute():
        print("Command.execute()")

################################################################################
class Commands:
    commands = {}

################################################################################
def command_class(name):
    def _command_class(_class):
        Commands.commands[name] = _class
#        _class.parse()
#        _class.execute()
        return _class
    return _command_class
