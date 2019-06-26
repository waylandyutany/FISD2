from core.code_line import Code_line
from core.commands import command_class, Command

################################################################################
# FISD_STORE_CONTEXT Command
################################################################################
@command_class()
class Fisd_store_context_command(Command):
    _keyword = 'fisd_store_context'

    @staticmethod
    def parse(pargs):
        pass    

    @staticmethod
    def execute(eargs):
        eargs.context.store_context(eargs.args.value(0))

################################################################################
# FISD_RESTORE_CONTEXT Command
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

################################################################################
# FISD_CURRENT_FOLDER Command
################################################################################
@command_class()
class Fisd_current_folder_command(Command):
    _keyword = 'fisd_current_folder'

    @staticmethod
    def parse(pargs):
        pass    

    @staticmethod
    def execute(eargs):
        eargs.context.set_return_value(eargs.context.execution.current_file_folder())

################################################################################
# FISD_CURRENT_FILE Command
################################################################################
@command_class()
class Fisd_current_file_command(Command):
    _keyword = 'fisd_current_file'

    @staticmethod
    def parse(pargs):
        pass    

    @staticmethod
    def execute(eargs):
        eargs.context.set_return_value(eargs.context.execution.current_file_name())

################################################################################
# FISD_LINE_NUMBER Command
################################################################################
@command_class()
class Fisd_line_number_command(Command):
    _keyword = 'fisd_line_number'

    @staticmethod
    def parse(pargs):
        pass    

    @staticmethod
    def execute(eargs):
        eargs.context.set_return_value(eargs.context.execution.current_line_number())
