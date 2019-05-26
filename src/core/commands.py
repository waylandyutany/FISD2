from core.logger import Logger
################################################################################
class Command:
    @staticmethod
    def parse():
        Logger.log.info("Command.parse()")

    @staticmethod
    def execute(context, arguments):
        Logger.log.info("Command.execute()")

################################################################################
class Commands:
    commands = {}

################################################################################
def command_class(name):
    def _command_class(_class):
        Commands.commands[name] = _class
        return _class
    return _command_class
