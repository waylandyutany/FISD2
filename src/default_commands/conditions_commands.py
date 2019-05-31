from core.commands import command_class, Command
from default_commands.keywords import Keywords

################################################################################
# IF Command
################################################################################
@command_class(Keywords._IF)
class IfCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        pass

    @classmethod
    def execute(cls, context, arguments):
        pass

################################################################################
# ENDIF Command
################################################################################
@command_class(Keywords._END_IF)
class EndIfProcCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        pass

    @classmethod
    def execute(cls, context, arguments):
        pass

################################################################################
# ELSE Command
################################################################################
@command_class(Keywords._ELSE)
class ElseProcCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        pass

    @classmethod
    def execute(cls, context, arguments):
        pass

################################################################################
# ELIF Command
################################################################################
@command_class(Keywords._ELIF)
class ElifProcCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        pass

    @classmethod
    def execute(cls, context, arguments):
        pass

