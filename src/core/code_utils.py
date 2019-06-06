import core.code_keys as code_keys


################################################################################
import math

_eval_funcs = {'cos':math.cos,
                'sin':math.sin,
                }

def evaluate_string(s):
    return eval(s, {'__builtins__':None}, _eval_funcs)

################################################################################
def search_keywords_in_tokens(tokens, keywords):#@ move to Tokens class
    ret = []
    for i in range(0, len(tokens)):
        for keyword in keywords:
            if tokens.is_keyword(i) and tokens.is_value_no_case(i, keyword):
                ret.append(i)
    return ret

def mark_tokens_as_keywords(tokens, keywords):#@ move to Tokens class
    for i in range(0, len(tokens)):
        if tokens.is_name(i):
            for keyword in keywords:
                if tokens.is_value_no_case(i, keyword):
                    tokens.mark_as_keyword(i)

def evaluate_tokens(tokens, start_index, end_index):
    str_to_evaluate = " ".join((tokens.value_str(i) for i in range(start_index + 1, end_index)))
    return evaluate_string(str_to_evaluate)

################################################################################
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
################################################################################

