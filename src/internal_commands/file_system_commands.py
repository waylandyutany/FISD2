from core.commands import command_class, Command

################################################################################
# FILE_COUNT_LINE Command
################################################################################
@command_class('file_count_line')
class File_count_lineCommand(Command):
    @classmethod
    def execute(cls, params):
        params.logger.info("{}({})".format(cls._keyword, str(params.raw_args)))
