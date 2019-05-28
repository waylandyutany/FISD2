class Arguments:
    def __init__(self, tokens):
        self.__tokens = tokens

class Context:
    def __init__(self, code, logger):
        self.__code = code
        self.__logger = logger

    def run(self):
        pass
