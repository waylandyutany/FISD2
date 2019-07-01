from copy import deepcopy
from core.tokens import Tokens

################################################################################
class EvaluatedArguments: 
    def __init__(self, raw_args):
        self.__args = []

        #@todo works only for valid (...) calls !!! not for set !!!
        arg_tokens = Tokens(deepcopy(raw_args.tokens()))
        left_bracket_index = arg_tokens.find_op('(')
        if left_bracket_index != None:
            arguments = arg_tokens.pop_tokens(left_bracket_index,len(arg_tokens) - 1).split_tokens_by_op(',')
            for argument in arguments:
                if not argument.empty():
                    argument_name = None

                    if argument.is_name(0) and argument.is_op_value(1, '='): # name = value
                        argument_name = argument.value(0)
                        argument.pop_tokens(-1, 2)
                    elif argument.is_keyword(0) and argument.is_op_value(1, '(') == False: # name(
                        argument_name = argument.value(0)
                        argument.pop_tokens(-1, 1)

                    try:
                        argument_value = argument.evaluate()
                        self.__add(argument_name, argument_value, argument.to_string())
                    except:
                        self.__add(argument_name, None, argument.to_string())


    def __str__(self):
        return str(self.__args)

    def __len__(self):
        return len(self.__args)

    def __add(self, name, value, eval_str):
        self.__args.append((name, value, eval_str, type(value)))

    def __get(self, index, type):
        try:return self.__args[index][type]
        except:return None

    def name(self, index):
        return self.__get(index, 0)

    def value(self, index):
        return self.__get(index, 1)

    def eval_string(self, index):
        return self.__get(index, 2)

    def type(self, index):
        return self.__get(index, 3)

    def clone(self):
        return deepcopy(self)
