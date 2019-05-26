from core.tokens import Tokenizers, Tokens
from core.logger import Logger

################################################################################
class Code:
    def __init__(self):
        pass

    def compile_from_file(self, file_name):
        Logger.log.info("compile_from_file({})".format(file_name))
        with open(file_name) as f:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1

                tokens = Tokens(line)
                Tokenizers.tokenize(tokens)

                if not tokens.empty():
                    Logger.log.info("line {} : {}".format(line_number, tokens.tokens))
