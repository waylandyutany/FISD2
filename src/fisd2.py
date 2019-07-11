import sys, os, glob2, argparse
import core.core as core

from core.context import Context
from core.tokens import Tokenizers
from core.code.code_compilation import Code_compilation

from core.commands.commands import Commands
from core.logger import Logger

from testing.testing import Testing

from core.safe_utils import safe_log_params
from core.utils import TimeLogger, log_exception

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
# 2. self._exit, what if call run_code again ? Assert or context restart, or what?
# 3. error test_assert('non existing function') never fails !!! test_assert(count_file_lines(report_file_path, "*TOTAL_CASES - 2*") == 1, "")
# 4. warning if merging report json stat file
# 5. Nicer bin json + zipped
# 6. this_name, main_name
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
def run_from_bin_fisd_file(fisd_file_name, logger, delete_bin_file):
    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Restoring '{}'...".format(fisd_file_name), 
                    "Restoring duration", logger.debug):
        context.restore_context(fisd_file_name)

    if logger._errors > 0:return

    with TimeLogger("Running '{}'...".format(fisd_file_name), 
                    "Running duration", logger.debug):
        context.run_from_restored_context()

    if delete_bin_file:
        logger.info("Removing binary fisd file '{}'...".format(fisd_file_name))
        os.remove(fisd_file_name)

################################################################################
#--fisd-file test/**/tc_*.fisd2 test/**/tc_*.bin --test-report-file reports/report.txt

if __name__ == '__main__':
    logger = None

    try:
        parser = argparse.ArgumentParser(description="")
        parser.add_argument('--fisd-file', type=str, nargs='*', action='store', help='')
        parser.add_argument('--compile-to-file', action='store_true', default=False, help='')
        parser.add_argument('--delete-bin-file', action='store_true', default=False, help='Binary fisd file is deleted after processed.')
        parser.add_argument('--test-report-file', type=str, default=None, help='Report file will be generated.')
        parser.add_argument('--merge-report-file', action='store_true', default=False, help='Merge report file from previous run.')
        parser.add_argument('--log-file', default=None, type=str, help='')
        parser.add_argument('--log-verbosity', default='info', type=str, choices=['debug', 'info', 'warning', 'error', 'critical'], help='')
        args = parser.parse_args()

        #Initialize logging
        Logger.init_logger(args.log_file, args.log_verbosity, args.test_report_file)
        logger = Logger(Logger.log)

        #Initialize testing
        Testing.init(args.test_report_file, args.merge_report_file, logger)

        with TimeLogger("{} version '{}'...".format(core.__app_name__, core.__app_version__), 
                        "Total '{}' duration".format(core.__app_name__), logger.info):

            safe_log_params(logger.info, "Command line : ", sys.argv)

            files_to_process = []
            for fisd_file in args.fisd_file:
                if os.path.isfile(fisd_file):
                    files_to_process.append(fisd_file)
                else:
                    files_to_process.extend(glob2.glob(fisd_file))
            #files_to_process = sorted(files_to_process)

            for file_name in files_to_process:
                file_extension = str(os.path.splitext(file_name)[1]).lower()
                logger.reset_errors()
                logger.reset_criticals()

                if os.path.isfile(file_name):
                    logger.info("Processing '{}'...".format(file_name))
                else:
                    # Skipping file processing in case file has been meanwhile deleted by other fisd file
                    logger.info("Skipping '{}'...".format(file_name))
                    continue

                if file_extension in core.__binary_fisd_file_extensions__:
                    run_from_bin_fisd_file(file_name, logger, args.delete_bin_file)
                else:
                    if args.compile_to_file:
                        compile_to_file(file_name, logger)
                    else:
                        run_from_fisd_file(file_name, logger)

        #Finalize testing, logging and saving reports and stats
        Testing.finalize()
    except Exception as e:
        #logger.critical(str(e) + " - " + str(sys.exc_info()))
        log_exception(logger.critical) if logger else log_exception(print)
        raise
