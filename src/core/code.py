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
        self.__code_path = None

################################################################################
    def __find_fisd_file(self, file_name):
        dir_name = os.path.dirname(file_name)
        name, ext = os.path.splitext(os.path.basename(file_name))

        possible_files = []
        if len(dir_name) == 0:
            dir_name = self.__code_path
        if len(ext) == 0:
            possible_files.append(os.path.join(dir_name, name) + '.fisd')
            possible_files.append(os.path.join(dir_name, name) + '.fisd2')
        else:
            possible_files.append(os.path.join(dir_name, name) + ext)

        for possible_file in possible_files:
            if os.path.isfile(possible_file):
                return os.path.basename(possible_file), os.path.abspath(possible_file)

        return None, None

    def __process_execute_tokens(self, tokens, logger):
        if tokens.is_name(0) and tokens.is_value_no_case(0, Keywords._EXECUTE):
            if not tokens.is_string(1):
                logger.error("Valid fisd file name must follow 'execute' command!")
                return
            tokenized_file_name = self.__tokenize_from_file(tokens.value_str(1), logger)
            if tokenized_file_name:
                tokens.set_string(1, tokenized_file_name)

################################################################################
    def __tokenize_from_file(self, _file_name, logger):
        file_name, file_path = self.__find_fisd_file(_file_name)
        if not file_name:
            logger.error("Non existing file '{}'!".format(_file_name))
            return file_name

        if file_name in self.code[Code._FILES]:
            return file_name
        self.code[Code._FILES][file_name] = {}

        logger.info("Compiling fisd file '{}'...".format(file_path))

        with open(file_path ) as f:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1
                logger.preface = "'{}'[{}] : ".format(file_name, line_number)

                tokens = Tokens(line)
                Tokenizers.tokenize(tokens)

                self.__process_execute_tokens(tokens, logger)

                logger.preface = "'{}'[{}] : ".format(file_name, line_number)
                if not tokens.empty():
                    self.code[Code._FILES][file_name][line_number] = tokens.tokens
                    logger.info("{}".format(tokens.tokens))

        return file_name
################################################################################
    def compile_from_file(self, file_name, logger):
        self.__code_path = os.path.dirname(file_name)
        self.__tokenize_from_file(file_name, logger)
