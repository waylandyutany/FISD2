from core.commands import command_class, Command
import fnmatch
from core.safe_utils import safe_file_delete

################################################################################
# FILE_COUNT_LINE Command
################################################################################
@command_class('file_count_lines')
class File_count_linesCommand(Command):
    #@todo need to have option for case sensitive matching 
    @classmethod
    def execute(cls, params):
        line_counter = 0
        file_name = params.evaluated_args.value(0)
        line_match_pattern = params.evaluated_args.value(1)
        with open(file_name) as f:
            for line in f.readlines():
                # padding begin and end with ' ' in order to fix matching entire line
                if fnmatch.fnmatch(" " + line + " ", line_match_pattern):
                    line_counter += 1

        params.set_return(line_counter)

################################################################################
# FILE_DELETE Command
################################################################################
@command_class('file_delete')
class File_deleteCommand(Command):
    @classmethod
    def execute(cls, params):
        file_path = params.evaluated_args.value(0)
        params.set_return(safe_file_delete(file_path))
