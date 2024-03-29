from core.code.code_line import Code_line
from core.code.call_signature import Call_signature

import inspect

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

    @classmethod
    def get_call_signature(cls):
        if not cls._callable:
            return None
        if not cls._call_signature:
            cls._call_signature = Call_signature.create_from_signature(inspect.signature(cls.call))
        return cls._call_signature

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
def command_class(keyword=None, cmd_type=None):
    def _command_class(_class):
        if keyword != None:
            setattr(_class, '_keyword', keyword)

        if cmd_type != None:
            setattr(_class, '_cmd_type', cmd_type)
           
        setattr(_class, '_callable', hasattr(_class, 'call'))
        setattr(_class, '_call_signature', None)
        
        # making sure all keywords are lower case
        _class._keyword = str(_class._keyword).lower()

        Commands.commands[_class._keyword] = _class

        return _class

    return _command_class

################################################################################
def call_command(execution_params):
    if execution_params.command_class._callable:
        ret = execution_params.command_class.call(execution_params, *execution_params.evaluated_args.values())
        execution_params.set_return(ret)
    else:
        execution_params.command_class.execute(execution_params)
