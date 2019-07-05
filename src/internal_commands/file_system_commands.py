from core.commands import command_class, Command
import os

################################################################################
# FILE_COUNT_LINE Command
################################################################################
@command_class('file_count_lines')
class File_count_linesCommand(Command):
    @classmethod
    def execute(cls, params):
        line_counter = 0
        file_name = params.evaluated_args.value(0)
        line_match_pattern = params.evaluated_args.value(1)
        with open(file_name) as f:
            for line in f.readlines():
                if line_match_pattern in line:
                    line_counter += 1

        params.set_return(line_counter)

################################################################################
# FILE_DELETE Command
################################################################################
@command_class('file_delete')
class File_deleteCommand(Command):
    @classmethod
    def execute(cls, params):
        file_name = params.evaluated_args.value(0)
        try:
            os.remove(file_name)
            params.set_return(True)
        except:
            params.set_return(False)
