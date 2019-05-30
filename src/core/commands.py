################################################################################
class Command:
    @staticmethod
    def parse(tokens, logger):
        raise NotImplementedError("Abstract method!")

    @staticmethod
    def execute(context, arguments, logger):
        raise NotImplementedError("Abstract method!")

################################################################################
class Commands:
    commands = {}

################################################################################
def command_class(name):
    def _command_class(_class):
        Commands.commands[str(name).lower()] = _class
        return _class
    return _command_class
