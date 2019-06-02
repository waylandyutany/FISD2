import core.code_keys as code_keys

def split_code_line(code_line):
    ''' Split stored code line and returns it's line_number, line_tokens, command_class '''
    return code_line[code_keys._LINE_NUMBER], code_line[code_keys._TOKENS], code_line[code_keys._COMMAND_CLASS]

def filter_code_lines(code_lines, filters):
    ret = []
    for i in range(0, len(code_lines)):
        line_number, line_tokens, _ = split_code_line(code_lines[i])
        for filter in filters:
            if line_tokens.is_name(0) and line_tokens.is_value_no_case(0, filter):
                ret.append((line_number, line_tokens))
    return ret

def move_code_lines(code_lines, first_line_number, last_line_number):
    ret = []
    from_index = 0
    to_index = len(code_lines)
    while from_index < to_index:
        line_number, _, _ = split_code_line(code_lines[from_index])
        if first_line_number <= line_number and line_number <= last_line_number:
            ret.append(code_lines[from_index])
            del code_lines[from_index]
            to_index -= 1
        else:
            from_index += 1

    return ret

