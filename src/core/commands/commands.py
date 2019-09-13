from core.code.code_line import Code_line

################################################################################
class Command:
    #Any token with name in this list is automaticaly marked as keyword.
    _keywords = None
    _keyword = None
    _cmd_type = None

    @classmethod
    def parse(cls, pargs):
        pass
        #pargs.logger.error("Command '{}'.parse is not yet implemented!".format(cls._keyword))

    @classmethod
    def execute(cls, eargs, *args, **kwargs):
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
def command_class(keyword=None, cmd_type=None, pass_evaluated_args = False):
    def _command_class(_class):
        if keyword != None:
            setattr(_class, '_keyword', keyword)

        if cmd_type != None:
            setattr(_class, '_cmd_type', cmd_type)

        # if _pass_evaluated_args True, evaluated arguments are passed within execute(cls, params, ...)
        # and returned value is automaticaly set to context
        setattr(_class, '_pass_evaluated_args', pass_evaluated_args)
           
        Commands.commands[str(_class._keyword).lower()] = _class

        return _class
    return _command_class

################################################################################
def call_command(execution_params):
    if execution_params.command_class._pass_evaluated_args:
        ret = execution_params.command_class.execute(execution_params, *execution_params.evaluated_args.values())
        execution_params.set_return(ret)
    else:
        execution_params.command_class.execute(execution_params)
