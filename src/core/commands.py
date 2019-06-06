################################################################################
class ParseArgs:
    def __init__(self, _code, _logger):
        self.code_name = None
        self.code_line = None
        self.code = _code
        self.logger = _logger
        self.code_lines = None
        self.code_index = None

################################################################################
class ExecuteArgs: 
    def __init__(self, _context):
        self.context = _context
        self.arguments = None
        self.code_lines = None
        self.code_index = None

################################################################################
class Command:

    #Any token with name in this list is automaticaly marked as keyword.
    _keywords = None

    @staticmethod
    def parse(parse_args):
        raise NotImplementedError("Abstract method!")

    @staticmethod
    def execute(execute_args):
        raise NotImplementedError("Abstract method!")

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
def command_class(name):
    def _command_class(_class):
        Commands.commands[str(name).lower()] = _class
        return _class
    return _command_class
