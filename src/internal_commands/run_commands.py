from core.commands import command_class, Command

################################################################################
# RUN Command
################################################################################
@command_class()
class RunCommand(Command):
    _keyword = 'run'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.error("Not implemented yet!")

################################################################################
# RUN_ASYNC Command
################################################################################
@command_class()
class Run_asyncCommand(Command):
    _keyword = 'run_async'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.error("Not implemented yet!")

################################################################################
# KILL_ASYNC Command
################################################################################
@command_class()
class Kill_asyncCommand(Command):
    _keyword = 'kill_async'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.error("Not implemented yet!")
