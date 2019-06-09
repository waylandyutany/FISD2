################################################################################
import math

_eval_funcs = {'cos':math.cos,
                'sin':math.sin,
                }

def evaluate_string(s):
    return eval(s, {'__builtins__':None}, _eval_funcs)

def evaluate_tokens(tokens, start_index, end_index):
    str_to_evaluate = " ".join((tokens.value_str(i) for i in range(start_index + 1, end_index)))
    return evaluate_string(str_to_evaluate)


################################################################################
