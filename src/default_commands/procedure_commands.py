from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME, TOKEN_OP
from core.code_line import Code_line

################################################################################
# PROC Command
################################################################################
@command_class()
class ProcCommand(Command):
    _keyword = 'proc'

    @staticmethod
    def parse(pargs):
        #@ error when missing begin and end parenthesis
        # mark all names as keywords, we do value replacement on execute
        _, line_tokens, _ = Code_line.split(pargs.code_line)
        for i in range(0, len(line_tokens)):
            if line_tokens.is_name(i):
                line_tokens.mark_as_keyword(i)

    @staticmethod
    def execute(eargs):
        #@todo handle different parameters and default parameters
        variable_tokens = eargs.arguments.sub_tokens(eargs.arguments.find_op('('), eargs.arguments.find_op(')'))
        value_tokens = eargs.context.pop_call_tokens()
        for i in range(0, len(variable_tokens)):
            if variable_tokens.is_keyword(i):
                eargs.context.set_variable(variable_tokens.value(i), value_tokens.value(i))

################################################################################
# END_PROC Command
################################################################################
@command_class()
class EndProcCommand(Command):
    _keyword = 'endproc'

    @staticmethod
    def parse(pargs):
        pass

    @staticmethod
    def execute(eargs):
        pass

################################################################################
# RETURN Command
################################################################################
@command_class()
class ReturnCommand(Command):
    _RETURN = 'return'
    _keyword = _RETURN

    @staticmethod
    def parse(pargs):
        pass

    @staticmethod
    def execute(eargs):
        pass

################################################################################
# CALL Command
################################################################################
@command_class()
@tokenizer_class()
class CallCommand(Command):
    _CALL = 'call'
    _keyword = _CALL

    @staticmethod
    def parse(pargs):
        pass

    @staticmethod
    def execute(eargs):
        i0 = eargs.arguments.find_op('(')
        i1 = eargs.arguments.find_op(')')
        call_tokens = eargs.arguments.sub_tokens(i0, i1)
        eargs.context.push_call_tokens(call_tokens)
        eargs.context.execute_code(eargs.arguments.value_str(1))

    @staticmethod
    def tokenize(tokens, logger):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '('):
            tokens.insert_name(0, CallCommand._keyword)
