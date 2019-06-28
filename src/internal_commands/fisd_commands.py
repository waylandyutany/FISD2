from core.commands import command_class, Command

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
# FISD_CURRENT_FOLDER Command
################################################################################
@command_class('fisd_current_folder')
class Fisd_current_folder_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(params.context.execution.current_file_folder())

################################################################################
# FISD_CURRENT_FILE Command
################################################################################
@command_class('fisd_current_file')
class Fisd_current_file_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(params.context.execution.current_file_name())

################################################################################
# FISD_LINE_NUMBER Command
################################################################################
@command_class('fisd_line_number')
class Fisd_line_number_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(params.context.execution.current_line_number())
