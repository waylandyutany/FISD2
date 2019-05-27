from core.tokens import Tokenizers, Tokens
from default_commands.keywords import Keywords
import os

################################################################################
class Code:
    _FILES = 'files'
    _FUNCTIONS = 'functions'

################################################################################
    def __init__(self):
        self.code = {Code._FILES:{}, Code._FUNCTIONS:{}}
        self.code_path = None

################################################################################
    def __find_fisd_file(self, file_name):
        if not self.code_path:
            self.code_path = os.path.dirname(file_name)

        return file_name, os.path.abspath(file_name)

    def __process_execute_tokens(self, tokens, logger):
        pass

    def __process_tokens(self, tokens, logger):
        self.__process_execute_tokens(tokens, logger)

################################################################################
    def compile_from_file(self, file_name, logger):
        file_name, file_path = self.__find_fisd_file(file_name)
        if not file_name:
            return
        if file_name in self.code[Code._FILES]:
            return
        self.code[Code._FILES][file_name] = {}

        logger.info("Compiling from file '{}'...".format(file_path))

        with open(file_path ) as f:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1
                logger.preface = "'{}'[{}] : ".format(file_name, line_number)

                tokens = Tokens(line)
                Tokenizers.tokenize(tokens)

                self.__process_tokens(tokens, logger)

                if not tokens.empty():
                    self.code[Code._FILES][file_name][line_number] = tokens.tokens
                    logger.info("{}".format(tokens.tokens))

        return True
