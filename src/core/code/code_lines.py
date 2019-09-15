from core.code.code_line import Code_line
from core.code.code import Code
from core.code.call_signature import Call_signature

class Code_lines:
    @staticmethod
    def filter(code_lines, filters):
        ret = []
        for i in range(0, len(code_lines)):
            line_number, line_tokens, _ = Code_line.split(code_lines[i])
            if line_tokens.is_name(0) and line_tokens.is_value_no_case(0, filters):
                ret.append((line_number, line_tokens))
        return ret

    @staticmethod
    def move(code_lines, first_line_number, last_line_number):
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


    @staticmethod
    def create():
        return {Code._CODE_LINES:[]}

    @staticmethod
    def create_function_code_lines(function_file_name, function_code_lines):
        return {Code._CODE_LINES:function_code_lines,
                Code._FUNCTION_FILE_NAME:function_file_name,
                Code._FUNCTION_CALL_SIGNATURE:Call_signature.create_from_function_code_lines(function_code_lines).to_json_dict()}

    @staticmethod
    def get_code_lines(code):
        return code[Code._CODE_LINES]
