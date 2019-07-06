from core.commands import command_class, Command
import subprocess, psutil

################################################################################
# RUN Command
################################################################################
@command_class('run')
class RunCommand(Command):
    @classmethod
    def log_run_params(cls, logger_func, message, run_params):
        if len(run_params) > 0:
            logger_func(message + "'{}'".format(run_params[0]))
            for i in range(1, len(run_params)):
                logger_func((" " * len(message)) + "'{}'".format(run_params[i]))

    @classmethod
    def get_run_params(cls, params):
        eargs = params.evaluated_args
        return [str(eargs.value(i)) for i in range(0,len(eargs))]

    @classmethod
    def execute(cls, params):
        run_params = cls.get_run_params(params)
        cls.log_run_params(params.logger.info, "Run : ", run_params)
        process = subprocess.Popen(run_params)
        response = process.communicate()

################################################################################
# RUN_ASYNC Command
################################################################################
@command_class('run_async')
class Run_asyncCommand(Command):
    @classmethod
    def execute(cls, params):
        run_params = RunCommand.get_run_params(params)
        RunCommand.log_run_params(params.logger.info, "Run async : ", run_params)
        subprocess.Popen(run_params)
        params.set_return(str(run_params))
        #params.logger.info("Running async '{}'...".format(run_params))

################################################################################
# KILL_ASYNC Command
################################################################################
@command_class('kill_async')
class Kill_asyncCommand(Command):
    @classmethod
    def execute(cls, params):
        run_params = eval(params.evaluated_args.value(0))
        RunCommand.log_run_params(params.logger.info, "Kill async : ", run_params)

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['cmdline','pid'])
                try:
                    if pinfo['cmdline'] == run_params:
                        proc.terminate()
                        params.set_return(True)
                        return
                    #if all((pinfo['cmdline'][i] == run_params[i]) for i in range(0,len(run_params))):
                    #    #params.logger.info("Killing {}.".format(pinfo['pid']))
                    #    proc.terminate()
                    #    params.set_return(True)
                    #    return
                except:
                    pass
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        params.set_return(False)
        params.logger.error("Unable to kill async process {}!".format(str(run_params)))
