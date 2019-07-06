################################################################################
class TestingStat:
    def __init__(self, logger):
        self.__logger = logger
        pass

    @property
    def logger(self):
        return self.__logger

    def begin_test_suite(self, name, description):
        pass

    def begin_test_set(self, name, description):
        pass    

    def begin_test_case(self, name, description):
        pass
