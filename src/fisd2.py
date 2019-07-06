import sys, os, glob2, traceback, argparse
import core.core as core

from core.context import Context
from core.tokens import Tokenizers
from core.code_compilation import Code_compilation
from core.commands import Commands
from core.logger import Logger
from core.utils import TimeLogger
from testing.testing import Testing

#importing all default command files
import internal_commands.default_commands
import internal_commands.loop_commands
import internal_commands.conditions_commands
import internal_commands.procedure_commands
import internal_commands.evaluation_commands
import internal_commands.fisd_commands
import internal_commands.this_commands
import internal_commands.file_system_commands
import internal_commands.run_commands
import testing.testing_commands
import internal_commands.time_commands

################################################################################
#@todos
# 1. time_start, time_delay and use it for wait tc
#
################################################################################

def compile_to_file(fisd_file_name, logger):
    fisd_bin_file_name = fisd_file_name + ".bin"

    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Compiling '{}' to '{}'...".format(fisd_file_name, fisd_bin_file_name),
                    "Compilation duration", logger.debug): 
        code.compile_from_file(fisd_file_name, logger)

    if logger._errors > 0:return

    with TimeLogger("Storing to '{}'...".format(fisd_file_name, fisd_bin_file_name),
                    "Storing duration", logger.debug):
        context.store_context(fisd_bin_file_name)

################################################################################
def run_from_fisd_file(fisd_file_name, logger):
    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Compiling '{}'...".format(fisd_file_name),
                    "Compilation duration", logger.debug):
        code.compile_from_file(fisd_file_name, logger)

    if logger._errors > 0:return

    with TimeLogger("Running '{}'...".format(fisd_file_name), 
                    "Running duration", logger.debug):
        context.run()

################################################################################
def run_from_bin_fisd_file(fisd_file_name, logger):
    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Restoring '{}'...".format(fisd_file_name), 
                    "Restoring duration", logger.debug):
        context.restore_context(fisd_file_name)

    if logger._errors > 0:return

    with TimeLogger("Running '{}'...".format(fisd_file_name), 
                    "Running duration", logger.debug):
        context.run_from_restored_context()

################################################################################
if __name__ == '__main__':
    logger = None

    try:
        parser = argparse.ArgumentParser(description="")
        parser.add_argument('--fisd-file', type=str, help='')
        parser.add_argument('--compile-to-file', action='store_true', help='')
        parser.add_argument('--test-report-file', type=str, default=None, help='')
        parser.add_argument('--log-file', default=None, type=str, help='')
        parser.add_argument('--log-verbosity', default='info', type=str, choices=['debug', 'info', 'warning', 'error', 'critical'], help='')
        args = parser.parse_args()

        #Initialize logging
        Logger.init_logger(args.log_file, args.log_verbosity, args.test_report_file)
        logger = Logger(Logger.log)

        #Initialize testing
        Testing.init(args.test_report_file, logger)

        logger.info("'{}'".format(str(sys.argv)))

        with TimeLogger("{} version '{}'...".format(core.__app_name__, core.__app_version__), 
                        "Total '{}' duration".format(core.__app_name__), logger.info):

            files_to_process = []
            if os.path.isfile(args.fisd_file):
                files_to_process = [args.fisd_file]
            else:
                files_to_process = glob2.glob(args.fisd_file)

            for file_name in files_to_process:
                file_extension = str(os.path.splitext(file_name)[1]).lower()
                logger.reset_errors()

                if file_extension in core.__binary_fisd_file_extensions__:
                    run_from_bin_fisd_file(file_name, logger)
                else:
                    if args.compile_to_file:
                        compile_to_file(file_name, logger)
                    else:
                        run_from_fisd_file(file_name, logger)

        #Finalize testing, logging and saving reports and stats
        Testing.finalize()
    except Exception as e:
        #logger.critical(str(e) + " - " + str(sys.exc_info()))
        exc_type, exc_value, exc_traceback = sys.exc_info()
        for trace_line in reversed(traceback.format_exception(exc_type, exc_value, exc_traceback)[1:]):
            if logger:
                logger.critical(str(trace_line)[:-1])
            else:
                print(str(trace_line)[:-1])
        raise
