from core.code_line import Code_line

################################################################################
class ParseParams:
    def __init__(self, _code, _logger, _code_name):
        self.code_name = _code_name
        self.code_index = None

        self.code = _code
        self.logger = _logger

        self.code_lines_insertion = Code_lines_insertion()
        self.code_labels = Code_labels()
        self.code_lines = self.code.get_code_lines(_code_name)

    @property
    def code_line(self):
        return self.code_lines[self.code_index]

    @property
    def line_number(self):
        return Code_line.get_line_number(self.code_line)

    @property
    def line_tokens(self):
        return Code_line.get_line_tokens(self.code_line)

    @property
    def command_name(self):
        return self.line_tokens.value(0)

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
class Code_labels:
    def __init__(self):
        self._labels_counter = {}
       
    def get_label_name(self, label_name):
        if label_name not in self._labels_counter:
            self._labels_counter[label_name] = 0
            return "{}_{:02d}".format(label_name, self._labels_counter[label_name])

        self._labels_counter[label_name] += 1
        return "{}_{:02d}".format(label_name, self._labels_counter[label_name])
