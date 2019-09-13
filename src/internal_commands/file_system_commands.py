from core.commands.commands import command_class, Command
from core.safe_utils import safe_file_delete
from core.commands.command_type import CallableCommand as Callable

import fnmatch

################################################################################
# FILE_COUNT_LINE Command
################################################################################
@command_class('file_count_lines', Callable(), True)
class File_count_linesCommand(Command):
    #@todo need to have option for case sensitive matching 
    @classmethod
    def execute(cls, params, file_name, line_match_pattern):
        line_counter = 0
        with open(file_name) as f:
            for line in f.readlines():
                # padding begin and end with ' ' in order to fix matching entire line
                if fnmatch.fnmatch(" " + line + " ", line_match_pattern):
                    line_counter += 1

        return line_counter

################################################################################
# FILE_DELETE Command
################################################################################
@command_class('file_delete', Callable(), True)
class File_deleteCommand(Command):
    @classmethod
    def execute(cls, params, file_path):
        return safe_file_delete(file_path)
