from core.logger import Logger
################################################################################
class Command:
    @staticmethod
    def parse(tokens, logger):
        Logger.log.info("Command.parse({})".format(tokens))

    @staticmethod
    def execute(context, arguments, logger):
        Logger.log.info("Command.execute()")

################################################################################
class Commands:
    commands = {}

################################################################################
def command_class(name):
    def _command_class(_class):
        Commands.commands[str(name).lower()] = _class
        return _class
    return _command_class
