from core.commands import command_class, Command
from default_commands.keywords import Keywords

################################################################################
# PROC Command
################################################################################
@command_class(Keywords._PROC)
class ProcCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, context, arguments):
        pass

################################################################################
# END_PROC Command
################################################################################
@command_class(Keywords._END_PROC)
class EndProcCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, context, arguments):
        pass

################################################################################
# RETURN Command
################################################################################
@command_class(Keywords._RETURN)
class ReturnCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, context, arguments):
        pass

