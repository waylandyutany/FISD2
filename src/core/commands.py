################################################################################
class ParseArgs:
    def __init__(self, _code, _logger):
        self.code_name = None
        self.code_lines = None
        self.code_index = None
        self.code_line = None
        self.code_labels = None

        self.code = _code
        self.logger = _logger

        self.code_lines_insertion = None

################################################################################
class ExecuteArgs: 
    def __init__(self, _context, _logger, _code_name, _code_lines):
        self.code_name = _code_name
        self.code_lines = _code_lines
        self.code_index = None
        self.code_line = None

        self.arguments = None

        self.context = _context
        self.logger = _logger

################################################################################
class Command:

    #Any token with name in this list is automaticaly marked as keyword.
    _keywords = None
    _keyword = None
    _evaluate = False #if true function calls are evaluated

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
def command_class(name=None):
    def _command_class(_class):
        Commands.commands[str(_class._keyword).lower()] = _class
        return _class
    return _command_class
