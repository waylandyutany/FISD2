import parser, sys, os, glob
import core.core as core

from core.context import Context
from core.tokens import Tokenizers
from core.code_compilation import Code_compilation
from core.commands import Commands
from core.logger import Logger
from core.utils import TimeLogger

#importing all default command files
import default_commands.default_commands
import default_commands.loop_commands
import default_commands.conditions_commands
import default_commands.procedure_commands
import default_commands.evaluation_commands
import default_commands.fisd_commands

################################################################################
# @todo
# 0. !!! fix preface mess !!!, error when multiple command classes under same name, or multiple names under same command classes !!!
# 1. store_context from fisd, from cmd switch, for one and multiple files, with file_name specified with automatical file name from code name(for one and multiple files :-))
# 2. store context folder can be overwritten with cmd argument and with fisd command
################################################################################

################################################################################
Logger.init_logger()
logger = Logger(Logger.log)

################################################################################
def compile_to_file(fisd_file_name, logger):
    fisd_bin_file_name = fisd_file_name + ".bin"
    Logger.log.info("Compiling '{}' to '{}'...".format(fisd_file_name, fisd_bin_file_name))

    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Compilation time", Logger.log):
        code.compile_from_file(fisd_file_name, logger)

    with TimeLogger("Storing time", Logger.log):
        context.store_context(fisd_bin_file_name)

################################################################################
def run_from_fisd_file(fisd_file_name, logger):
    Logger.log.info("Running '{}'...".format(fisd_file_name))
    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Compilation time", Logger.log):
        code.compile_from_file(fisd_file_name, logger)

    with TimeLogger("Run time", Logger.log):
        context.run()

################################################################################
def run_from_bin_fisd_file(fisd_file_name, logger):
    Logger.log.info("Running '{}'...".format(fisd_file_name))
    code = Code_compilation()
    context = Context(code, logger)

    with TimeLogger("Restoring time", Logger.log):
        context.restore_context(fisd_file_name)

    with TimeLogger("Run time", Logger.log):
        context.run_from_restored_context()

################################################################################
if __name__ == '__main__':
    Logger.log.info("{} version '{}'.".format(core.__app_name__, core.__app_version__))

    args = sys.argv[1:]
    options = [str(arg).lower().strip(' -\t\n\r') for arg in args]
    Logger.log.info("Arguments {}".format(args))
    Logger.log.info("Options {}".format(options))

    #if wrong arguments or explicitly help required, help will be printed and script teminated
    print_help = False
    if len(args) == 0 or len({'help','?','h'}.intersection(set(options))) > 0:
        print_help = True

    if print_help:
        Logger.log.info("print_help")
        sys.exit(0)

    Logger.log.debug("Tokenizers {}.".format(", ".join(["'{}'".format(name) for name in Tokenizers.tokenizers])))
    Logger.log.debug("Commands {}.".format(", ".join(["'{}'".format(name) for name in Commands.commands])))

    for file_name in glob.glob(args[0]):
        file_extension = str(os.path.splitext(file_name)[1]).lower()
        logger.reset_errors()

        if file_extension in core.__fisd_file_extensions__:
            if 'compile-to-file' in options:
                compile_to_file(file_name, logger)
            else:
                run_from_fisd_file(file_name, logger)
        elif file_extension in core.__binary_fisd_file_extensions__:
            run_from_bin_fisd_file(file_name, logger)

        if logger._errors > 0:
            continue
