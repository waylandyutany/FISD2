from core.commands.commands import command_class, Command
from core.commands.command_type import CallableCommand as Callable
import datetime, time

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

        if  time_to_seconds >= 3600:
            hours = int(time_to_seconds/3600)
            minutes = int((time_to_seconds - (hours*3600)) / 60)
            seconds = int(time_to_seconds - (hours*3600) - (minutes*60))
            wait_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        elif time_to_seconds >= 60:
            minutes = int(time_to_seconds/60)
            seconds = int(time_to_seconds - (minutes * 60))
            wait_string = "{:02d}:{:02d}".format(minutes, seconds)
        else:
            wait_string = "{:02d}".format(int(time_to_seconds))

        float_part = int((time_to_seconds - int(time_to_seconds))*100)
        wait_string = wait_string + ".{:02d}".format(float_part)

        params.logger.info("Waiting {}...".format(wait_string))
        time.sleep(float(time_to_seconds))
        params.logger.info("Continuing after {} wait.".format(wait_string))

################################################################################
# DATE Command
################################################################################
@command_class('date')
class DateCommand(Command):
    @classmethod
    def call(cls, params):
        return datetime.datetime.now().strftime("%Y-%m-%d")

################################################################################
# TIME Command
################################################################################
@command_class('time')
class TimeCommand(Command):
    @classmethod
    def call(cls, params):
        return datetime.datetime.now().strftime("%H:%M:%S")

