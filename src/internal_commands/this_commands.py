from core.commands import command_class, Command

################################################################################
# THIS_FOLDER_NAME Command
################################################################################
@command_class('this_folder_name')
class This_folder_name_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(params.context.execution.current_file_folder())

################################################################################
# THIS_FILE_PATH Command
################################################################################
@command_class('this_file_path')
class This_file_path_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(params.context.execution.current_file_path())

################################################################################
# THIS_FILE_NAME Command
################################################################################
@command_class('this_file_name')
class This_file_name_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(params.context.execution.current_file_name())

################################################################################
# THIS_LINE_NUMBER Command
################################################################################
@command_class('this_line_number')
class This_line_number_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(params.context.execution.current_line_number())

################################################################################
# THIS_MAKE_PATH Command
################################################################################
@command_class('this_make_path')
class This_make_path_command(Command):
    @staticmethod
    def execute(params):
        eargs = params.evaluated_args
        params.context.set_return_value(params.context.execution.current_make_path(eargs.value(0)))
