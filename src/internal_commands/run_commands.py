from core.commands import command_class, Command
import subprocess, psutil, os, signal

################################################################################
# RUN Command
################################################################################
@command_class('run')
class RunCommand(Command):
    @classmethod
    def get_run_params(cls, params):
        eargs = params.evaluated_args
        return [str(eargs.value(i)) for i in range(0,len(eargs))]

    @classmethod
    def execute(cls, params):
        run_params = cls.get_run_params(params)
        process = subprocess.Popen(run_params,stdout=subprocess.PIPE)
        response = process.communicate()

################################################################################
# RUN_ASYNC Command
################################################################################
@command_class('run_async')
class Run_asyncCommand(Command):
    @classmethod
    def execute(cls, params):
        run_params = RunCommand.get_run_params(params)
        subprocess.Popen(run_params, stdout=subprocess.PIPE, shell=True)
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

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['cmdline','pid'])
                try:
                    if all((pinfo['cmdline'][i] == run_params[i]) for i in range(0,len(run_params))):
                        #params.logger.info("Killing {}.".format(pinfo['pid']))
                        proc.terminate()
                        params.set_return(True)
                        return
                except:
                    pass
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        params.set_return(False)
        params.logger.error("Unable to kill async process {}!".format(str(run_params)))
