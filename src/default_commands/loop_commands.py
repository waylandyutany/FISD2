from core.commands import command_class, Command
from default_commands.keywords import Keywords

################################################################################
# FOR Command
################################################################################
@command_class(Keywords._FOR)
class ForCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        pass

    @classmethod
    def execute(cls, context, arguments):
        pass

################################################################################
# NEXT Command
################################################################################
@command_class(Keywords._NEXT)
class NextProcCommand(Command):
    @classmethod
    def parse(cls, tokens, logger):
        pass

    @classmethod
    def execute(cls, context, arguments):
        pass

