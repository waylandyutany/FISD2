import parser, sys, os, glob
from datetime import datetime

from core.context import Context
from core.tokens import Tokenizers
from core.code_compilation import Code_compilation
from core.commands import Commands
from core.logger import Logger

#importing all default command files
import default_commands.default_commands
import default_commands.loop_commands
import default_commands.conditions_commands
import default_commands.procedure_commands
import default_commands.evaluation_commands
import default_commands.fisd_commands

################################################################################
# @todo
# 1. store_context from fisd, from cmd switch, for one and multiple files, with file_name specified with automatical file name from code name(for one and multiple files :-))
# 2. store context folder can be overwritten with cmd argument and with fisd command
################################################################################
__app_name__ = 'FISD2'
__app_version__ = '2.0.0'

################################################################################
Logger.init_logger()
logger = Logger(Logger.log)

################################################################################
def compile_to_file(fisd_file_name, logger):
    fisd_bin_file_name = fisd_file_name + ".bin"
    logger.info("Compiling '{}' to '{}'...".format(fisd_file_name, fisd_bin_file_name))

    code = Code_compilation()
    context = Context(code, logger)

    start_compilation_time = datetime.now()
    #code compilation from file
    code.compile_from_file(fisd_file_name, logger)
    compilation_time = datetime.now() - start_compilation_time
    logger.info("Compilation time '{}'.".format(compilation_time))

    start_store_time = datetime.now()
    context.store_context(fisd_bin_file_name)
    store_time = datetime.now() - start_store_time
    logger.info("Storing time '{}'.".format(store_time))

def run_from_fisd_file(fisd_file_name, logger):
    logger.info("Running '{}'...".format(fisd_file_name))
    code = Code_compilation()
    context = Context(code, logger)

    start_compilation_time = datetime.now()
    #code compilation from file
    code.compile_from_file(fisd_file_name, logger)
    compilation_time = datetime.now() - start_compilation_time
    logger.info("Compilation time '{}'.".format(compilation_time))

    start_run_time = datetime.now()
    context.run(logger)
    run_time = datetime.now() - start_run_time
    logger.info("Run time '{}'.".format(run_time))

################################################################################
if __name__ == '__main__':
    Logger.log.info("{} version '{}'.".format(__app_name__, __app_version__))

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
        logger.reset_errors()

        if 'compile-to-file' in options:
            compile_to_file(file_name, logger)
        else:
            run_from_fisd_file(file_name, logger)

        if logger._errors > 0:
            continue
