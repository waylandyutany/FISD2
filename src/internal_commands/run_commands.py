from core.commands import command_class, Command

################################################################################
# RUN Command
################################################################################
@command_class('run')
class RunCommand(Command):
    @classmethod
    def execute(cls, params):
        eargs = params.evaluated_args
        run_params = " ".join(str(eargs.value(i)) for i in range(0,len(eargs)))
        params.logger.info("Running '{}'...".format(run_params))

################################################################################
# RUN_ASYNC Command
################################################################################
@command_class('run_async')
class Run_asyncCommand(Command):
    @classmethod
    def execute(cls, params):
        params.logger.error("Not implemented yet!")

################################################################################
# KILL_ASYNC Command
################################################################################
@command_class('kill_async')
class Kill_asyncCommand(Command):
    @classmethod
    def execute(cls, params):
        params.logger.error("Not implemented yet!")
