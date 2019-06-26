from core.commands import command_class, Command

################################################################################
# FILE_COUNT_LINE Command
################################################################################
@command_class()
class File_count_lineCommand(Command):
    _keyword = 'file_count_line'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("{}({})".format(cls._keyword, str(eargs.arguments)))
