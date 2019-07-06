################################################################################
class TestingStat:
    _tag_test_suite = "#TEST_SUITE"
    _tag_test_set = "#TEST_SET"
    _tag_test_case = "#TEST_CASE"

    def __init__(self, logger):
        self.__logger = logger
        pass

    @property
    def logger(self):
        return self.__logger

    def begin_test_suite(self, name, description):
        self.logger.info("{} '{}'...".format(TestingStat._tag_test_suite, name))

    def begin_test_set(self, name, description):
        self.logger.info("{} '{}'...".format(TestingStat._tag_test_set, name))

    def begin_test_case(self, name, description):
        self.logger.info("{} '{}'...".format(TestingStat._tag_test_case, name))
