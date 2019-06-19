from core.code_line import Code_line
from core.commands import command_class, Command

################################################################################
# STORE_CONTEXT Command
################################################################################
@command_class()
class Fisd_store_context_command(Command):
    _keyword = 'fisd_store_context'

    @staticmethod
    def parse(pargs):
        pass    

    @staticmethod
    def execute(eargs):
        eargs.context.store_context(eargs.arguments.value_str(1) if eargs.arguments.value(1) else None)

################################################################################
# RESTORE_CONTEXT Command
################################################################################
@command_class()
class Fisd_restore_context_command(Command):
    _keyword = 'fisd_restore_context'

    @staticmethod
    def parse(pargs):
        pass    

    @staticmethod
    def execute(eargs):
        pass
