from core.commands.commands import command_class, Command
import os

################################################################################
def normalize_path(path):
    return path.replace("\\","/")

def get_file_name_from_path(path):
    return os.path.split(path)[1]

def get_folder_name_from_path(path):
    file_path, _ = os.path.split(path)
    _, folder_name = os.path.split(file_path)
    return folder_name

def make_path_from_path(from_path, path):
    from_path, _ = os.path.split(from_path)
    return normalize_path(os.path.abspath(os.path.join(from_path, path)))

################################################################################
# THIS_FOLDER_NAME Command
################################################################################
@command_class('this_folder_name')
class This_folder_name_command(Command):
    @staticmethod
    def execute(params):
        context = params.context
        context.set_return_value(get_folder_name_from_path(context.execution.current_code_path))

################################################################################
# THIS_FILE_PATH Command
################################################################################
@command_class('this_file_path')
class This_file_path_command(Command):
    @staticmethod
    def execute(params):
        context = params.context
        context.set_return_value(normalize_path(context.execution.current_code_path))

################################################################################
# THIS_FILE_NAME Command
################################################################################
@command_class('this_file_name')
class This_file_name_command(Command):
    @staticmethod
    def execute(params):
        context = params.context
        context.set_return_value(get_file_name_from_path(context.execution.current_code_path))

################################################################################
# THIS_LINE_NUMBER Command
################################################################################
@command_class('this_line_number')
class This_line_number_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(params.context.execution.current_line_number)

################################################################################
# MAKE_PATH_FROM_THIS Command
################################################################################
@command_class('make_path_from_this')
class Make_path_from_this_command(Command):
    @staticmethod
    def execute(params):
        context = params.context
        eargs = params.evaluated_args
        context.set_return_value(make_path_from_path(context.execution.current_code_path,
                                                     eargs.value(0)))

################################################################################
# MAIN_FILE_NAME Command
################################################################################
@command_class('main_file_name')
class Main_file_name_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(get_file_name_from_path(params.code.main_code_name()))

################################################################################
# MAIN_FILE_PATH Command
################################################################################
@command_class('main_file_path')
class Main_file_path_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(normalize_path(params.code.main_code_name()))

################################################################################
# MAIN_FOLDER_NAME Command
################################################################################
@command_class('main_folder_name')
class Main_folder_name_command(Command):
    @staticmethod
    def execute(params):
        params.context.set_return_value(get_folder_name_from_path(params.code.main_code_name()))

################################################################################
# MAKE_PATH_FROM_MAIN Command
################################################################################
@command_class('make_path_from_main')
class Make_path_from_main_command(Command):
    @staticmethod
    def execute(params):
        eargs = params.evaluated_args
        params.context.set_return_value(make_path_from_path(params.code.main_code_name(),
                                                            eargs.value(0)))
