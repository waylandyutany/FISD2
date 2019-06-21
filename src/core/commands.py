################################################################################
class Command:

    #Any token with name in this list is automaticaly marked as keyword.
    _keywords = None
    _keyword = None
    _evaluate = False #if true function calls are evaluated

    @staticmethod
    def parse(pargs):
        raise NotImplementedError("Abstract method!")

    @classmethod
    def execute(cls, eargs):
        eargs.logger.error("Command '{}' is not yet implemented!".format(cls._keyword))

################################################################################
class Commands:
    commands = {}

    @classmethod
    def find_command(cls, name):
        name = str(name).lower()
        if name in cls.commands:
            return cls.commands[name]
        return None

################################################################################
def command_class(name=None):
    def _command_class(_class):
        Commands.commands[str(_class._keyword).lower()] = _class
        return _class
    return _command_class
