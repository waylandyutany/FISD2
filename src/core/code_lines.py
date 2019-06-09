import core.code_keys as code_keys
from core.code_line import Code_line

class Code_lines:
    @classmethod
    def filter(cls, code_lines, filters):
        ret = []
        for i in range(0, len(code_lines)):
            line_number, line_tokens, _ = Code_line.split(code_lines[i])
            if line_tokens.is_name(0) and line_tokens.is_value_no_case(0, filters):
                ret.append((line_number, line_tokens))
        return ret

    @classmethod
    def move(cls, code_lines, first_line_number, last_line_number):
        ret = []
        from_index = 0
        to_index = len(code_lines)
        while from_index < to_index:
            line_number, _, _ = Code_line.split(code_lines[from_index])
            if first_line_number <= line_number and line_number <= last_line_number:
                ret.append(code_lines[from_index])
                del code_lines[from_index]
                to_index -= 1
            else:
                from_index += 1

        return ret
