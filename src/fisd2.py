import parser, sys
from core.context import Context

context = Context()

if __name__ == '__main__':
    args = sys.argv[1:]
    options = [str(arg).lower().strip(' -\t\n\r') for arg in args]
    print(args)
    print(options)
