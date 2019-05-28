from core.tokens import Tokenizers, Tokens
from default_commands.keywords import Keywords
from core.commands import Commands
import os

################################################################################
class Code:
    _FILES = 'files'
    _FUNCTIONS = 'functions'
    _TOKENS = 'tokens'
    _COMMAND = 'command'

################################################################################
    def __init__(self):
        self.__code = {Code._FILES:{}, Code._FUNCTIONS:{}}
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

        if file_name in self.__code[Code._FILES]:
            return file_name
        self.__code[Code._FILES][file_name] = {}

        logger.info("Compiling fisd file '{}'...".format(file_path))

        with open(file_path ) as f:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1

                tokens = Tokens(line)
                Tokenizers.tokenize(tokens)

                logger.preface = "'{}'[{}] : ".format(file_name, line_number)
                self.__process_execute_tokens(tokens, logger)
                logger.preface = "'{}'[{}] : ".format(file_name, line_number)

                if not tokens.empty():
                    self.__code[Code._FILES][file_name][line_number] = {Code._TOKENS:None, Code._COMMAND:None}
                    self.__code[Code._FILES][file_name][line_number][Code._TOKENS] = tokens
                    logger.info("{}".format(tokens.tokens()))

        return file_name

    def __parse_commands(self, logger):
        for code_file in self.__code[Code._FILES]:
            for code_line in self.__code[Code._FILES][code_file]:
                line_tokens = self.__code[Code._FILES][code_file][code_line][Code._TOKENS]

                logger.preface = "'{}'[{}] : ".format(code_file, code_line)

                if not line_tokens.is_name(0):
                    logger.error("Invalid command token {}!".format(line_tokens.value(0)))
                    continue

                command_class = Commands.commands[line_tokens.value(0).lower()]
                if not command_class:
                    logger.error("Invalid command {}!".format(line_tokens.value(0)))
                    continue;

                self.__code[Code._FILES][code_file][code_line][Code._COMMAND] = command_class
                command_class.parse(line_tokens, logger)

################################################################################
    def compile_from_file(self, file_name, logger):
        self.__code_path = os.path.dirname(file_name)
        self.__tokenize_from_file(file_name, logger)
        self.__parse_commands(logger)
