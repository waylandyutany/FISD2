import parser, sys, os

from core.context import Context
from core.code import Tokenizers, Code
from core.commands import Commands
import default_commands.default_commands

################################################################################
context = Context()
code = Code()

################################################################################
if __name__ == '__main__':
    args = sys.argv[1:]
    options = [str(arg).lower().strip(' -\t\n\r') for arg in args]
    print(args)
    print(options)

    #if wrong arguments or explicitly help required, help will be printed and script teminated
    print_help = False
    if len(args) == 0 or len({'help','?','h'}.intersection(set(options))) > 0:
        print_help = True

    if print_help:
        print("print_help")
        sys.exit(0)

    print("Tokenizers : {}".format(Tokenizers.tokenizers))
    print("Commands : {}".format(Commands.commands))

    #code compilation from file
    if os.path.isfile(args[0]):
        code.compile_from_file(args[0])
