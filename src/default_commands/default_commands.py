from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME
from core.code_line import Code_line

################################################################################
# SET Command
################################################################################
@command_class()
@tokenizer_class()
class SetCommand(Command):
    _SET = 'set'
    _keyword = _SET

    @classmethod
    def parse(cls, parse_args):
        _, line_tokens, _ = Code_line.split(parse_args.code_line)
        line_tokens.mark_as_keyword(1)

    @classmethod
    def execute(cls, execute_args):
        variable_name = execute_args.arguments.value(1)
        try:
            evaluated_value = execute_args.arguments.evaluate_tokens(2, len(execute_args.arguments))
        except Exception as e:
            execute_args.logger.error("Exception during expression '{} = {}' evaluation! {}!".format(variable_name, string_to_evaluate, e))
            return

        #context.logger.debug("'{}' evaluated '{} = {}'".format(variable_name, string_to_evaluate, evaluated_value))

        execute_args.context.set_variable(variable_name, evaluated_value)

    @classmethod
    def tokenize(cls, tokens, logger):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '='):
            tokens.insert_name(0, cls._SET)

################################################################################
# PRINT Command
################################################################################
@command_class()
class PrintCommand(Command):
    _PRINT = 'print'
    _keyword = _PRINT

    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        execute_args.logger.info("PRINT {}".format("".join( ( str(execute_args.arguments.value_str(i)) for i in range(1, len(execute_args.arguments)) ) )))

################################################################################
# EXECUTE Command
################################################################################
@command_class()
class ExecuteCommand(Command):
    _EXECUTE = 'execute'
    _keyword = _EXECUTE

    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        execute_args.context.execute_code(execute_args.arguments.value_str(1))

