import parser, sys, os

from core.context import Context
from core.code import Tokenizers, Code
from core.commands import Commands
from core.logger import Logger
import default_commands.default_commands

################################################################################
# @todo
#   1. recursive compile_for_file for each execute statement
#   2. handle set command with context
#   3. handle print command
#   4. handle execute command
#
################################################################################
__app_name__ = 'FISD2'
__app_version__ = '2.0.0'

################################################################################
context = Context()
code = Code()

Logger.init_logger()
################################################################################
if __name__ == '__main__':
    Logger.log.info("{} version {}".format(__app_name__, __app_version__))

    args = sys.argv[1:]
    options = [str(arg).lower().strip(' -\t\n\r') for arg in args]
    Logger.log.info("Arguments : {}".format(args))
    Logger.log.info("Options : {}".format(options))

    #if wrong arguments or explicitly help required, help will be printed and script teminated
    print_help = False
    if len(args) == 0 or len({'help','?','h'}.intersection(set(options))) > 0:
        print_help = True

    if print_help:
        Logger.log.info("print_help")
        sys.exit(0)

    Logger.log.info("Tokenizers : {}".format(", ".join(["'{}'".format(name) for name in Tokenizers.tokenizers])))
    Logger.log.info("Commands : {}".format(", ".join(["'{}'".format(name) for name in Commands.commands])))

    #code compilation from file
    if os.path.isfile(args[0]):
        logger = Logger(Logger.log)
        code.compile_from_file(args[0], logger)
