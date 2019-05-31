from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME
from core.logger import Logger
from default_commands.keywords import Keywords

################################################################################
# SET Command
################################################################################
@command_class(Keywords._SET)
@tokenizer_class(Keywords._SET)
class SetCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        tokens.mark_as_keyword(1)
        pass

    @classmethod
    def execute(cls, context, arguments, logger):
        variable_name = arguments.value(1)
        string_to_evaluate = " ".join( arguments.value(i) for i in range(3,len(arguments)))
        variable_value = eval(string_to_evaluate, {'__builtins__':None}, {})
        logger.info("'{}' evaluated '{} = {}'".format(variable_name, string_to_evaluate, variable_value))
        context.set_variable(variable_name, variable_value)

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

