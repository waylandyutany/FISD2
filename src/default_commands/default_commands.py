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
        tokens.set_keyword(1)
        #logger.debug("SetCommand.parse({})".format(tokens))
        pass

    @classmethod
    def execute(cls, context, arguments, logger):
        #logger.debug("SetCommand.execute({})".format(arguments))
        pass

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
        #logger.debug("PrintCommand.parse({})".format(tokens))
        pass

    @classmethod
    def execute(cls, context, arguments, logger):
        #logger.debug("PrintCommand.execute({})".format(arguments))
        logger.info("PRINT {}".format("".join( ( arguments.value_str(i) for i in range(1, len(arguments)) ) )))

################################################################################
# EXECUTE Command
################################################################################
@command_class(Keywords._EXECUTE)
class ExecuteCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        #logger.debug("ExecuteCommand.parse({})".format(tokens))
        pass

    @classmethod
    def execute(cls, context, arguments, logger):
        #logger.debug("ExecuteCommand.execute({})".format(arguments))
        context.execute_code(arguments.value_str(1), logger)

