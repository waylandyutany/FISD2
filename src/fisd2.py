import parser, sys, os, glob2, traceback
import core.core as core

from core.context import Context
from core.tokens import Tokenizers
from core.code_compilation import Code_compilation
from core.commands import Commands
from core.logger import Logger
from core.utils import TimeLogger

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
import internal_commands.test_commands

################################################################################
# @todo

################################################################################
Logger.init_logger()
logger = Logger(Logger.log)

################################################################################
def compile_to_file(fisd_file_name, logger):
    fisd_bin_file_name = fisd_file_name + ".bin"
    Logger.log.info()

    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Compiling '{}' to '{}'...".format(fisd_file_name, fisd_bin_file_name),
                    "Compilation duration", logger): 
        code.compile_from_file(fisd_file_name, logger)

    if logger._errors > 0:return

    with TimeLogger("Storing to '{}'...".format(fisd_file_name, fisd_bin_file_name),
                    "Storing duration", logger):
        context.store_context(fisd_bin_file_name)

################################################################################
def run_from_fisd_file(fisd_file_name, logger):
    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Compiling '{}'...".format(fisd_file_name),
                    "Compilation duration", logger):
        code.compile_from_file(fisd_file_name, logger)

    if logger._errors > 0:return

    with TimeLogger("Running '{}'...".format(fisd_file_name), 
                    "Running duration", logger):
        context.run()

################################################################################
def run_from_bin_fisd_file(fisd_file_name, logger):
    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Restoring '{}'...".format(fisd_file_name), 
                    "Restoring duration", logger):
        context.restore_context(fisd_file_name)

    if logger._errors > 0:return

    with TimeLogger("Running '{}'...".format(fisd_file_name), 
                    "Running duration", logger):
        context.run_from_restored_context()

################################################################################
if __name__ == '__main__':
    try:
        #enable coloring on windows
        os.system('color')

        with TimeLogger("{} version '{}'...".format(core.__app_name__, core.__app_version__), 
                        "Total '{}' duration".format(core.__app_name__), logger):

            args = sys.argv[1:]
            options = [str(arg).lower().strip(' -\t\n\r') for arg in args]
            #Logger.log.info("Arguments {}".format(args))
            #Logger.log.info("Options {}".format(options))

            #if wrong arguments or explicitly help required, help will be printed and script teminated
            print_help = False
            if len(args) == 0 or len({'help','?','h'}.intersection(set(options))) > 0:
                print_help = True

            if print_help:
                Logger.log.info("print_help")
                sys.exit(0)

            #Logger.log.debug("Tokenizers {}.".format(", ".join(["'{}'".format(name) for name in Tokenizers.tokenizers])))
            #Logger.log.debug("Commands {}.".format(", ".join(["'{}'".format(name) for name in Commands.commands])))

            for file_name in glob2.glob(args[0]):
                file_extension = str(os.path.splitext(file_name)[1]).lower()
                logger.reset_errors()

                if file_extension in core.__fisd_file_extensions__:
                    if 'compile-to-file' in options:
                        compile_to_file(file_name, logger)
                    else:
                        run_from_fisd_file(file_name, logger)
                elif file_extension in core.__binary_fisd_file_extensions__:
                    run_from_bin_fisd_file(file_name, logger)

    except Exception as e:
        #logger.critical(str(e) + " - " + str(sys.exc_info()))
        exc_type, exc_value, exc_traceback = sys.exc_info()
        for trace_line in reversed(traceback.format_exception(exc_type, exc_value, exc_traceback)[1:]):
            logger.critical(str(trace_line)[:-1])
        raise
