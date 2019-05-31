from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME
from core.logger import Logger
from default_commands.keywords import Keywords
import math

################################################################################
# SET Command
################################################################################
@command_class(Keywords._SET)
@tokenizer_class(Keywords._SET)
class SetCommand(Command):
    _eval_funcs = {'cos':math.cos,
                   'sin':math.sin,
                   }

    @classmethod
    def parse(cls, tokens, logger):
        tokens.mark_as_keyword(1)
        pass

    @classmethod
    def execute(cls, context, arguments, logger):
        variable_name = arguments.value(1)
        string_to_evaluate = " ".join( str(arguments.value(i)) for i in range(3,len(arguments)))

        try:
            evaluated_value = eval(string_to_evaluate, {'__builtins__':None}, cls._eval_funcs)
        except Exception as e:
            logger.error("Exception during expression '{} = {}' evaluation! {}!".format(variable_name, string_to_evaluate, e))
            return

        logger.debug("'{}' evaluated '{} = {}'".format(variable_name, string_to_evaluate, evaluated_value))

        context.set_variable(variable_name, evaluated_value)

    @classmethod
    def tokenize(cls, tokens, logger):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '='):
            tokens.insert_name(0, 'set')

################################################################################
# PRINT Command
################################################################################
@command_class(Keywords._PRINT)
class PrintCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        pass

    @classmethod
    def execute(cls, context, arguments, logger):
        logger.info("PRINT {}".format("".join( ( str(arguments.value_str(i)) for i in range(1, len(arguments)) ) )))

################################################################################
# EXECUTE Command
################################################################################
@command_class(Keywords._EXECUTE)
class ExecuteCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        pass

    @classmethod
    def execute(cls, context, arguments, logger):
        context.execute_code(arguments.value_str(1), logger)

