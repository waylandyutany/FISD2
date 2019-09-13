from core.commands.commands import command_class, Command
from core.commands.command_type import CallableCommand as Callable

import sys

################################################################################
# FISD_STORE_CONTEXT Command
################################################################################
@command_class('fisd_store_context')
class Fisd_store_context_command(Command):
    @staticmethod
    def execute(params):
        params.context.store_context(params.evaluated_args.value(0))

################################################################################
# FISD_RESTORE_CONTEXT Command
################################################################################
@command_class('fisd_restore_context')
class Fisd_restore_context_command(Command):
    @staticmethod
    def execute(params):
        pass

################################################################################
# FISD_PLATFORM Command
################################################################################
@command_class('fisd_sys_platform', Callable())
class Fisd_sys_platform_command(Command):
    @staticmethod
    def execute_args(params):
        return sys.platform
