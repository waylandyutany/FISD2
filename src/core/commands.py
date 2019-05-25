class Command:
    @staticmethod
    def parse():
        print("Command.parse()")

    @staticmethod
    def execute():
        print("Command.execute()")

class Commands:
    commands = {}
    
def register_command_class(name, cmd_class):
    Commands.commands[name] = cmd_class
    print("{} : {}".format(name, cmd_class))
    cmd_class.parse()
    cmd_class.execute()

def command_class(name):
    def _command_class(cmd_class):
        register_command_class(name, cmd_class)
    return _command_class
