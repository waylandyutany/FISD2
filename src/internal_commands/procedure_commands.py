from core.commands import command_class, Command, Commands
from core.tokens import tokenizer_class, Tokens
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
        variable_names = eargs.raw_args.sub_tokens(eargs.raw_args.find_op('('), eargs.raw_args.find_op(')')).split_tokens_by_op(',')
        variable_values = eargs.context.pop_call_tokens().split_tokens_by_op(',')

        names = [str(tokens.value(0)) for tokens in variable_names if not tokens.empty()]
        evaluated_values = [tokens.evaluate() for tokens in variable_values if not tokens.empty()]

        #value_tokens = [token.evaluate() for token in variable_tokens]
        for i in range(0, len(names)):
            eargs.context.set_variable(names[i], evaluated_values[i])

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
        eargs.context.return_execute_code(None)

################################################################################
# RETURN Command
################################################################################
@command_class()
class ReturnCommand(Command):
    _keyword = 'return'

    @staticmethod
    def parse(pargs):
        pass

    @staticmethod
    def execute(eargs):
        if len(eargs.raw_args) > 1:
            value = eargs.raw_args.evaluate_tokens(0, len(eargs.raw_args))
            eargs.context.return_execute_code(value)
        else:
            eargs.context.return_execute_code(None)

################################################################################
# CALL Command
################################################################################
@command_class()
@tokenizer_class()
class CallCommand(Command):
    _keyword = 'call'

    @staticmethod
    def parse(pargs):
        #@todo error when mismatched number of arguments
        #@todo detect function calls and generate call and set_ret instructions
        pass

    @staticmethod
    def execute(eargs):
        i0 = eargs.raw_args.find_op('(')
        call_tokens = eargs.raw_args.sub_tokens(i0, len(eargs.raw_args) - 1)
        eargs.context.push_call_tokens(call_tokens)
        eargs.context.execute_code(eargs.raw_args.value_str(1))

    @staticmethod
    def tokenize(tokens, logger):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '(') and Commands.find_command(tokens.value(0)) == None:
            tokens.insert_name(0, CallCommand._keyword)

    @staticmethod
    def create_code_line(line_number, tokens):
        tokens.insert_name(0, CallCommand._keyword)
        tokens.mark_as_keyword(0)
        code_line = Code_line.create(line_number, tokens, CallCommand)
        return code_line