from core.code_line import Code_line

################################################################################
class Command:
    #Any token with name in this list is automaticaly marked as keyword.
    _keywords = None
    _keyword = None

    @classmethod
    def parse(cls, pargs):
        pass
        #pargs.logger.error("Command '{}'.parse is not yet implemented!".format(cls._keyword))

    @classmethod
    def execute(cls, eargs):
        eargs.logger.error("Command '{}' is not yet implemented!".format(cls._keyword))

    @classmethod
    def create_code_line(cls, line_number, tokens):
        assert tokens.value(0).lower() == cls._keyword, ""
        code_line = Code_line.create(line_number, tokens, cls)
        return code_line

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
def command_class(keyword=None):
    def _command_class(_class):
        if keyword != None:
            setattr(_class, '_keyword', keyword)
        Commands.commands[str(_class._keyword).lower()] = _class
        return _class
    return _command_class
