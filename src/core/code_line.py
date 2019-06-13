class Code_line:
    _CODE_LABEL = 'label'
    _CODE_JUMPS = 'jumps'
    _LINE_NUMBER = 'line'
    _TOKENS = 'tokens'
    _COMMAND_CLASS = 'command'

    @classmethod
    def create(cls, line_number, tokens, command_class):
        return {cls._LINE_NUMBER:line_number, cls._TOKENS:tokens, cls._COMMAND_CLASS:command_class}

    @classmethod
    def get_line_number(cls, code_line):
        return code_line[cls._LINE_NUMBER]

    @classmethod
    def get_line_tokens(cls, code_line):
        return code_line[cls._TOKENS]

    @classmethod
    def set_command_class(cls, code_line, command_class):
        code_line[cls._COMMAND_CLASS] = command_class

    @classmethod
    def split(cls, code_line):
        ''' Split stored code line and returns it's line_number, line_tokens, command_class '''
        return code_line[cls._LINE_NUMBER], code_line[cls._TOKENS], code_line[cls._COMMAND_CLASS]

    @classmethod
    def add_label(cls, code_line, label_name):
        if cls._CODE_LABEL not in code_line:
            code_line[cls._CODE_LABEL] = []
        if label_name not in code_line[cls._CODE_LABEL]:
            code_line[cls._CODE_LABEL].append(label_name)

    @classmethod
    def add_jump(cls, code_line, jump_name, label_name):
        if cls._CODE_JUMPS not in code_line:
            code_line[cls._CODE_JUMPS] = {}
        code_line[cls._CODE_JUMPS][jump_name] = label_name

    @classmethod
    def get_jump(cls, code_line, jump_name):
        if cls._CODE_JUMPS not in code_line:
            return None
        if jump_name not in code_line[cls._CODE_JUMPS]:
            return None
        return code_line[cls._CODE_JUMPS][jump_name]

    @classmethod
    def get_labels(cls, code_line):
        if cls._CODE_LABEL in code_line:
            return code_line[cls._CODE_LABEL]
        return []

    @classmethod
    def get_jumps(cls, code_line):
        if cls._CODE_JUMPS not in code_line:
            return {}
        return code_line[cls._CODE_JUMPS]
