################################################################################
class EvaluatedArguments: 
    def __init__(self):
        self.__args = []

    def __str__(self):
        return str(self.__args)

    def __len__(self):
        return len(self.__args)

    def add(self, name, value, eval_str):
        self.__args.append((name, value, eval_str))

    def __get(self, index, type):
        try:return self.__args[index][type]
        except:return None

    def name(self, index):
        return self.__get(index, 0)

    def value(self, index):
        return self.__get(index, 1)

    def eval_string(self, index):
        return self.__get(index, 2)

    def copy(self):
        return deepcopy(self)
