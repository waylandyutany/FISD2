from core.commands import command_class, Command
import subprocess, psutil, os

################################################################################
# RUN Command
################################################################################
@command_class('run')
class RunCommand(Command):
    @classmethod
    def get_run_params(cls, params):
        eargs = params.evaluated_args
        return " ".join(str(eargs.value(i)) for i in range(0,len(eargs)))

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
        process = subprocess.Popen(run_params, stdout=subprocess.PIPE, shell=True)
        params.set_return(process.pid)
        params.logger.info("Running async '{}' with pid'{}'...".format(run_params, process.pid))
        params.logger.info("os.getpid()'{}'...".format(os.getpid()))

################################################################################
# KILL_ASYNC Command
################################################################################
@command_class('kill_async')
class Kill_asyncCommand(Command):
    @classmethod
    def execute(cls, params):
        pid_to_kill = params.evaluated_args.value(0)
        params.logger.info("Killing async pid'{}'".format(pid_to_kill))
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'ppid', 'name', 'username','cmdline'])
                if "calc" in pinfo['name'].lower():
                    params.logger.info(pinfo)
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
