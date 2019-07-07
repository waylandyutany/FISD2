################################################################################
import math
import os

################################################################################
#@todo expand more functions !!!
_eval_funcs = {'cos':math.cos,
               'sin':math.sin,
              }

def safe_eval(eval_str):
    return eval(eval_str, {'__builtins__':None}, _eval_funcs)

################################################################################
def safe_file_delete(path):
    try:
        os.remove(path)
        return True
    except:pass    
    return False

################################################################################
def safe_log_params(logger_func, message, params):
    if len(params) > 0:
        logger_func(message + "'{}'".format(params[0]))
        for i in range(1, len(params)):
            logger_func((" " * len(message)) + "'{}'".format(params[i]))
