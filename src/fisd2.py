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

################################################################################
# @todo
# 1. Generalize logger preface
# 2. Handle function name existances between functions and files
# 3. error codes and descriptions
################################################################################
__app_name__ = 'FISD2'
__app_version__ = '2.0.0'

################################################################################
Logger.init_logger()
logger = Logger(Logger.log)

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
        Logger.log.info("Running '{}'...".format(file_name))
        code = Code_compilation()
        context = Context(code)

        start_compilation_time = datetime.now()
        #code compilation from file
        code.compile_from_file(file_name, logger)
        compilation_time = datetime.now() - start_compilation_time
        Logger.log.info("Compilation time '{}'.".format(compilation_time))
        if logger._errors > 0:
            continue

        start_run_time = datetime.now()
        context.run(logger)
        run_time = datetime.now() - start_run_time
        Logger.log.info("Run time '{}'.".format(run_time))
