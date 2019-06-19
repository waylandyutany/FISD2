from core.code_json import Code_json
from core.tokens import Tokenizers, Tokens
from core.commands import Commands, ParseArgs
from core.compile_errors import CompileError
from core.code_line import Code_line
from core.code_lines import Code_lines

import core.core as core

from default_commands.default_commands import ExecuteCommand
from default_commands.procedure_commands import ProcCommand, EndProcCommand
from default_commands.evaluation_commands import Code_evaluation

import os

################################################################################
################################################################################
class Code_lines_insertion:
    def __init__(self):
        self._insertion = {}

    def insert_before(self, line_number, code_line):
        self.__insert(-1, line_number, code_line)

    def insert_after(self, line_number, code_line):
        self.__insert(1, line_number, code_line)

    def __insert(self, where, line_number, code_line):
        if line_number not in self._insertion:
            self._insertion[line_number] = { -1 : [], 1 : []}
        self._insertion[line_number][where].append(code_line)

    def pop_lines_for_insertion(self, line_number):
        if line_number in self._insertion:
            ret = self._insertion[line_number][-1], self._insertion[line_number][1]
            del self._insertion[line_number]
            return ret
        return None

################################################################################
################################################################################
class Code_labels:
    def __init__(self):
        self._labels_counter = {}
       
    def get_label_name(self, label_name):
        if label_name not in self._labels_counter:
            self._labels_counter[label_name] = 0
            return "{}_{:02d}".format(label_name, self._labels_counter[label_name])

        self._labels_counter[label_name] += 1
        return "{}_{:02d}".format(label_name, self._labels_counter[label_name])

################################################################################
################################################################################
class Code_compilation(Code_json):
    def __init__(self):
        self._code_path = None
        return super().__init__()

################################################################################
    def find_fisd_file(self, file_name):
        dir_name = os.path.dirname(file_name)
        name, ext = os.path.splitext(os.path.basename(file_name))

        possible_files = []
        if len(dir_name) == 0:
            dir_name = self._code_path
        if len(ext) == 0:
            possible_files = [os.path.join(dir_name, name) + ext for ext in core.__fisd_file_extensions__]
        else:
            possible_files.append(os.path.join(dir_name, name) + ext)

        for possible_file in possible_files:
            if os.path.isfile(possible_file):
                return os.path.basename(possible_file), os.path.abspath(possible_file)

        return None, None

    def __process_execute_tokens(self, tokens, logger):
        if tokens.is_name(0) and tokens.is_value_no_case(0, ExecuteCommand._keyword):
            if not tokens.is_string(1):
                logger.error("Valid fisd file name must follow 'execute' command!")
                return
            tokenized_file_name = self.__tokenize_from_file(tokens.value_str(1), logger)
            if tokenized_file_name:
                tokens.set_string(1, tokenized_file_name)

################################################################################
    def __tokenize_from_file(self, _file_name, logger):
        file_name, file_path = self.find_fisd_file(_file_name)
        if not file_name:
            logger.error(CompileError.non_existing_file_name(_file_name))
            return file_name

        if file_name in self._code:
            return file_name
        self._code[file_name] = Code_lines.create()

        #logger.debug("Compiling fisd file '{}'...".format(file_path))

        with open(file_path ) as f:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1

                tokens = Tokens(line)

                #@todo do it more generic with better preface handling
                logger.preface = "'{}'[{}] : ".format(file_name, line_number)
                Tokenizers.tokenize(tokens, logger)

                logger.preface = "'{}'[{}] : ".format(file_name, line_number)
                self.__process_execute_tokens(tokens, logger)

                if not tokens.empty():
                    Code_lines.get_code_lines(self._code[file_name]).append(Code_line.create(line_number, tokens, None))

        return file_name

    def __parse_commands(self, logger):
        parse_args = ParseArgs(self, logger)

        for code_name in self._code:
            #code labels uniqueness is per code[code_name]
            parse_args.code_labels = Code_labels()
            parse_args.code_lines = self.get_code_lines(code_name)
            parse_args.code_lines_insertion = Code_lines_insertion()

            for parse_args.code_index in range(0, len(parse_args.code_lines)):
                code_line = parse_args.code_lines[parse_args.code_index]
                parse_args.code_name = code_name
                parse_args.code_line = code_line

                line_number, line_tokens, _ = Code_line.split(code_line)

                logger.preface = self.get_code_line_description(code_name, line_number)

                if not line_tokens.is_name(0):
                    logger.error(CompileError.invalid_command(line_tokens.value(0)))
                    continue

                command_class = Commands.find_command(line_tokens.value(0))
                if not command_class:
                    logger.error(CompileError.unknown_command(line_tokens.value(0)))
                    continue

                line_tokens.mark_as_keyword(0)
                if command_class._keywords:
                    line_tokens.mark_tokens_as_keywords(command_class._keywords)

                Code_line.set_command_class(code_line,command_class)
                if command_class._evaluate:
                    Code_evaluation.evaluate_function_calls(parse_args)
                command_class.parse(parse_args)

            self.__insert_code_lines(parse_args.code_lines, parse_args.code_lines_insertion)

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
                functions_code[function_name] = Code_lines.create_function_code_lines(function_name, function_code_lines)

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
    def compile_from_file(self, file_name, logger):
        ''' Compiling code from the file, looking for *.fisd/*.fisd2 in no extension provided.'''
        self._code_path = os.path.dirname(file_name)
        self._main_code_name = self.__tokenize_from_file(file_name, logger)
        self.__extract_functions(logger)
        self.__parse_commands(logger)
        self.__resolve_jumps(logger)
