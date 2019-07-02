from core.commands import command_class, Command

################################################################################
# FILE_COUNT_LINE Command
################################################################################
@command_class('file_count_lines')
class File_count_linesCommand(Command):
    @classmethod
    def execute(cls, params):
        params.logger.info("{}({})".format(cls._keyword, str(params.raw_args)))
        params.set_return(0)
