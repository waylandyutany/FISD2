import parser, sys, os
from io import BytesIO
from tokenize import tokenize, NUMBER, STRING, NAME, OP, COMMENT

types = { NUMBER : "NUMBER",
         STRING : "STRING",
         NAME : "NAME",
         OP : "OP",
         COMMENT : "COMMENT"
         }

from core.context import Context

context = Context()

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

    #file parsing and execution
    print(os.path.abspath(args[0]))
    if os.path.isfile(args[0]):
        with open(args[0]) as f:
            for line in f.readlines():
                result = []
                tokens = tokenize(BytesIO(line.encode('utf-8')).readline)
                for toknum, tokval, _, _, _  in tokens:
                    if toknum in types:
                        print(types[toknum], tokval)
                    else:
                        print("Unknown {} {}".format(toknum, tokval))
