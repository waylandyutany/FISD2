from core.commands import command_class, Command
import subprocess, psutil
from core.safe_utils import safe_eval, safe_log_params

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
        safe_log_params(params.logger.info, "Run : ", run_params)
        #stdout=subprocess.PIPE disable flooding my output with new process output
        process = subprocess.Popen(run_params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response = process.communicate()

################################################################################
# RUN_ASYNC Command
################################################################################
@command_class('run_async')
class Run_asyncCommand(Command):
    @classmethod
    def execute(cls, params):
        run_params = RunCommand.get_run_params(params)
        safe_log_params(params.logger.info, "Run async : ", run_params)
        #stdout=subprocess.PIPE disable flooding my output with new process output
        subprocess.Popen(run_params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        params.set_return(str(run_params))
        #params.logger.info("Running async '{}'...".format(run_params))

################################################################################
# KILL_ASYNC Command
################################################################################
@command_class('kill_async')
class Kill_asyncCommand(Command):
    @classmethod
    def execute(cls, params):
        run_params = safe_eval(params.evaluated_args.value(0))
        safe_log_params(params.logger.info, "Kill async : ", run_params)

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
