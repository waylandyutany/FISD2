################################################################################
class ParseParams:
    def __init__(self, _code, _logger):
        self.code_name = None
        self.code_lines = None
        self.code_index = None
        self.code_line = None
        self.code_labels = None

        self.code = _code
        self.logger = _logger

        self.code_lines_insertion = None

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
