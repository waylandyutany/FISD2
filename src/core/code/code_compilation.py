from core.code.code_json import Code_json
from core.code.code_line import Code_line
from core.code.code_lines import Code_lines
from core.code.parse_params import ParseParams, Code_lines_insertion, Code_labels

from core.tokens import Tokenizers, Tokens
from core.commands.commands import Commands
from core.compile_errors import CompileError
from core.utils import PrefaceLogger, folder_and_file_name
import core.core as core

from internal_commands.default_commands import ExecuteCommand
from internal_commands.procedure_commands import ProcCommand, EndProcCommand, CallCommand
from internal_commands.evaluation_commands import Code_evaluation

import os

################################################################################
################################################################################
class Code_compilation(Code_json):
    def __init__(self):
        return super().__init__()

################################################################################
    def __find_fisd_file(self, file_folder, file_name):
        file_names = [file_name]
        _, ext = os.path.splitext(os.path.basename(file_name))
        if len(ext) == 0:
            file_names = [file_name + ext for ext in core.__fisd_file_extensions__]

        possible_files = [os.path.join(file_folder, file_name) for file_name in file_names]
        for possible_file in possible_files:
            if os.path.isfile(possible_file):
                return os.path.abspath(possible_file)

        return None

    def __process_execute_tokens(self, file_folder, tokens, logger):
        if tokens.is_name(0) and tokens.is_value_no_case(0, ExecuteCommand._keyword):
            if not tokens.is_string(1):
                logger.error("Valid fisd file name must follow 'execute' command!")
                return
            tokenized_file_name = self.__tokenize_from_file(file_folder, tokens.value_str(1), logger)
            if tokenized_file_name:
                tokens.set_string(1, tokenized_file_name)

################################################################################
    def __tokenize_from_file(self, _file_folder, _file_name, logger):
        file_path = self.__find_fisd_file(_file_folder, _file_name)
        if not file_path:
            logger.error(CompileError.non_existing_file_name(_file_name))
            return file_path

        if file_path in self._code:
            return file_path
        logger.debug("Compiling '{}'...".format(folder_and_file_name(file_path)))

        self._code[file_path] = Code_lines.create()

        with open(file_path ) as f:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1

                tokens = Tokens(line)

                with PrefaceLogger("'{}'[{}] : ".format(folder_and_file_name(file_path), line_number), logger):
                    Tokenizers.tokenize(tokens, logger)

                with PrefaceLogger("'{}'[{}] : ".format(folder_and_file_name(file_path), line_number), logger):
                    self.__process_execute_tokens(os.path.dirname(file_path), tokens, logger)

                if not tokens.empty():
                    Code_lines.get_code_lines(self._code[file_path]).append(Code_line.create(line_number, tokens, None))

        return file_path

    def __parse_commands(self, logger):
        for code_name in self._code:
            #code labels uniqueness is per code[code_name]
            parse_params = ParseParams(self, logger, code_name)

            for parse_params.code_index in range(0, len(parse_params.code_lines)):
                with PrefaceLogger(self.get_code_line_description(code_name, parse_params.line_number), logger):
                    if not parse_params.command_name:
                        logger.error(CompileError.invalid_command(parse_params.command_name))
                        continue

                    command_class = Commands.find_command(parse_params.command_name)
                    if not command_class:
                        logger.error(CompileError.unknown_command(parse_params.command_name))
                        continue

                    parse_params.line_tokens.mark_as_keyword(0)
                    if command_class._keywords:
                        parse_params.line_tokens.mark_tokens_as_keywords(command_class._keywords)

                    Code_line.set_command_class(parse_params.code_line, command_class)

                    Code_evaluation.evaluate_function_calls(parse_params)

                    if command_class._cmd_type:
                        command_class._cmd_type.preprocess_line_tokens(parse_params.line_tokens)

                    command_class.parse(parse_params)

            self.__insert_code_lines(parse_params.code_lines, parse_params.code_lines_insertion)

    def __insert_code_lines(self, code_lines, insertion):
        #@todo move label if avaliable at the beginning of line with same line numbers !!!
        i = 0
        while i < len(code_lines):
            line_number = Code_line.get_line_number(code_lines[i])
            lines = insertion.pop_lines_for_insertion(line_number)
            if lines:
                lines_before, lines_after = lines
                code_lines[i+1:i+1] = lines_after
                code_lines[i:i] = lines_before
                i += len(lines_before) + len(lines_after)

            i += 1


    def __extract_functions(self, logger):
        #@todo error when end proc w/o proc keyword
        #@todo error when no name token after proc token
        #@todo error when function name already exists, we should allow same function name but not for same scope, but we should at least warn
        #@todo error when proc within proc, no nested proc supported
        #@todo error no endproc
        functions_code = {}
        for code_name in self._code:
            code_lines = self.get_code_lines(code_name)
            proc_code_lines = Code_lines.filter(code_lines, [ProcCommand._keyword, EndProcCommand._keyword])
            for i in range(0,len(proc_code_lines),2):
                first_line_number, first_line_tokens = proc_code_lines[i]
                last_line_number, last_line_tokens = proc_code_lines[i+1]
                function_name = first_line_tokens.value(1)
                function_code_lines = Code_lines.move(code_lines, first_line_number, last_line_number)
                functions_code[function_name] = Code_lines.create_function_code_lines(code_name, function_code_lines)

        for function_code in functions_code:
            self._code[function_code] = functions_code[function_code]
        pass

    def __resolve_jumps(self, logger):
        for code_name in self._code:
            code_lines = self.get_code_lines(code_name)

            labels_jumps_indicies = {}

            #searching for all labels and remember it's indicies
            for i in range(0, len(code_lines)):
                code_line = code_lines[i]
                labels = Code_line.get_labels(code_line)
                for label in labels:
                    assert label not in labels_jumps_indicies, "Each label must be unique !!!"
                    labels_jumps_indicies[label] = i

            #searching for all jump labels and replace label_name with code index
            for i in range(0, len(code_lines)):
                code_line = code_lines[i]
                jumps = Code_line.get_jumps(code_line)
                for jump_name in jumps:
                    jumps[jump_name] = labels_jumps_indicies[jumps[jump_name]]

################################################################################
    def __resolve_call_signatures(self, logger):
        ''' Checking call parameters match with function or command signature
Resolving default call paramaters e.g. option="case_sensitive"'''

        for code_name in self._code:
            parse_params = ParseParams(self, logger, code_name)
            for parse_params.code_index in range(0, len(parse_params.code_lines)):
                with PrefaceLogger(self.get_code_line_description(code_name, parse_params.line_number), logger):
                    command_class = Code_line.get_command_class(parse_params.code_line)

                    # checking against command call signature
                    if command_class._callable:
                        command_class._call_signature.resolve(logger, parse_params.line_tokens)

                    # checking against function signature
                    elif command_class._keyword == CallCommand._keyword:
                        call_signature = None
                        if call_signature:
                            call_signature.resolve(logger, parse_params.line_tokens)

################################################################################
    def compile_from_file(self, file_name, logger):
        ''' Compiling code from the file, looking for *.fisd/*.fisd2 in no extension provided.'''
        self._main_code_name = self.__tokenize_from_file(os.path.dirname(file_name), os.path.basename(file_name), logger)
        self.__extract_functions(logger)
        self.__parse_commands(logger)
        self.__resolve_jumps(logger)
        self.__resolve_call_signatures(logger)
