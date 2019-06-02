################################################################################
class ParseArgs:
    def __init__(self, _code, _logger):
        self.code_name = None
        self.code_line = None
        self.code = _code
        self.logger = _logger

################################################################################
class ExecuteArgs:
    def __init__(self):
        pass

################################################################################
class Command:
    @staticmethod
    def parse(parse_args):
        raise NotImplementedError("Abstract method!")

    @staticmethod
    def execute(context, arguments):
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
