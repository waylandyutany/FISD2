from core.tokens import Tokenizers, Tokens
from core.logger import Logger

################################################################################
class Code:
    _FILES = 'files'
    _FUNCTIONS = 'functions'

    def __init__(self):
        self.code = {Code._FILES:{}, Code._FUNCTIONS:{}}

    def is_compiled(self, file_name):
        return file_name in self.code[Code._FILES]

    def compile_from_file(self, file_name, logger):
        if self.is_compiled(file_name):
            return
        self.code[Code._FILES][file_name] = {}

        Logger.log.info("Compiling from file '{}'...".format(file_name))

        with open(file_name) as f:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1

                tokens = Tokens(line)
                Tokenizers.tokenize(tokens)

                if not tokens.empty():
                    self.code[Code._FILES][file_name][line_number] = tokens.tokens
                    Logger.log.info("line {} : {}".format(line_number, tokens.tokens))

        return True
