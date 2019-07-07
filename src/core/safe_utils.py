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
