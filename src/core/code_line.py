import core.code_keys as code_keys

class Code_line:
    _CODE_LABEL = 'label'
    _CODE_JUMPS = 'jumps'

    @staticmethod
    def create(line_number, tokens, command_class):
        return {code_keys._LINE_NUMBER:line_number, code_keys._TOKENS:tokens, code_keys._COMMAND_CLASS:command_class}

    @staticmethod
    def get_line_number(code_line):
        return code_line[code_keys._LINE_NUMBER]

    @staticmethod
    def split(code_line):
        ''' Split stored code line and returns it's line_number, line_tokens, command_class '''
        return code_line[code_keys._LINE_NUMBER], code_line[code_keys._TOKENS], code_line[code_keys._COMMAND_CLASS]

    @staticmethod
    def add_label(code_line, label_name):
        if Code_line._CODE_LABEL not in code_line:
            code_line[Code_line._CODE_LABEL] = []
        if label_name not in code_line[Code_line._CODE_LABEL]:
            code_line[Code_line._CODE_LABEL].append(label_name)

    @classmethod
    def add_jump(cls, code_line, jump_name, label_name):
        if Code_line._CODE_JUMPS not in code_line:
            code_line[Code_line._CODE_JUMPS] = {}
        code_line[Code_line._CODE_JUMPS][jump_name] = label_name

    @classmethod
    def get_jump(cls, code_line, jump_name):
        if Code_line._CODE_JUMPS not in code_line:
            return None
        if jump_name not in code_line[Code_line._CODE_JUMPS]:
            return None
        return code_line[Code_line._CODE_JUMPS][jump_name]

    @classmethod
    def get_labels(cls, code_line):
        if Code_line._CODE_LABEL in code_line:
            return code_line[Code_line._CODE_LABEL]
        return []

    @classmethod
    def get_jumps(cls, code_line):
        if Code_line._CODE_JUMPS not in code_line:
            return {}
        return code_line[Code_line._CODE_JUMPS]
