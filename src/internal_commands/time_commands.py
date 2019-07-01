from core.commands import command_class, Command
from core.command_type import CallableCommand as Callable
import datetime

################################################################################
# WAIT_TO_SECONDS Command
################################################################################
@command_class('time_to_seconds', Callable())
class Time_to_secondsCommand(Command):
    @staticmethod
    def string_to_seconds(s):
        float_part = 0.0
        time_and_float = s.split(".")
        try:float_part = float("0." + time_and_float[1])
        except:pass
        time_part = time_and_float[0].split(":")
        if len(time_part) == 3:
            return (int(time_part[0]) * 3600) + (int(time_part[1]) * 60) + int(time_part[0]) + float_part
        elif len(time_part) == 2:
            return (int(time_part[0]) * 60) + int(time_part[1]) + float_part
        elif len(time_part) == 1:
            return int(time_part[0]) + float_part
        return float_part

    @classmethod
    def time_to_seconds(cls, params):
        eargs = params.evaluated_args
        if len(eargs) == 3:
            return((eargs.value(0) * 3600) + (eargs.value(1) * 60) + eargs.value(2))
        elif len(eargs) == 2:
            return((eargs.value(0) * 60) + eargs.value(1))
        else:
            if eargs.type(0) == str:
                return(cls.string_to_seconds(eargs.value(0)))
            else:
                return(eargs.value(0))

    @classmethod
    def execute(cls, params):
        params.set_return(cls.time_to_seconds(params))

################################################################################
# WAIT Command
################################################################################
@command_class('wait', Callable())
class WaitCommand(Command):
    @classmethod
    def execute(cls, params):
        time_to_seconds = Time_to_secondsCommand.time_to_seconds(params)
        params.logger.info("Waiting '{}'s...".format(time_to_seconds))

################################################################################
# DATE Command
################################################################################
@command_class('date')
class DateCommand(Command):
    @classmethod
    def execute(cls, params):
        params.set_return(datetime.datetime.now().strftime("%Y-%m-%d"))

################################################################################
# TIME Command
################################################################################
@command_class('time')
class TimeCommand(Command):
    @classmethod
    def execute(cls, params):
        params.set_return(datetime.datetime.now().strftime("%H:%M:%S"))

