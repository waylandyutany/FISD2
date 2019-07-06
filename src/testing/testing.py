from testing.testing_stat import TestingStat

################################################################################
class Testing:
    _tag_test_suite = "#TEST_SUITE"
    _tag_test_set = "#TEST_SET"
    _tag_test_case = "#TEST_CASE"
    _tag_passed = "#PASSED"
    _tag_failed = "#FAILED"

    __stat = None
    __logger = None

    @classmethod
    def init(cls, report_file, logger):
        cls.__stat = TestingStat(logger)
        cls.__logger = logger

    @classmethod
    def finalize(cls):
        pass

    #@classmethod
    #def stat(cls):
    #    return cls.__stat

    @classmethod
    def begin_test_suite(cls, name, description):
        cls.__logger.info("{} '{}'...".format(cls._tag_test_suite, name))
        cls.__stat.begin_test_suite(name, description)

    @classmethod
    def begin_test_set(cls, name, description):
        cls.__logger.info("{} '{}'...".format(cls._tag_test_set, name))
        cls.__stat.begin_test_set(name, description)

    @classmethod
    def begin_test_case(cls, name, description):
        cls.__logger.info("{} '{}'...".format(cls._tag_test_case, name))
        cls.__stat.begin_test_case(name, description)

    @classmethod
    def test_assert(cls, evaluation, evaluation_string, evaluation_description):
        if evaluation == True:
            cls.__logger.info("{} '{}'".format(cls._tag_passed, 
                                               evaluation_description))
        else:
            cls.__logger.warning("{} '{}', {}".format(cls._tag_failed, 
                                                      evaluation_string,
                                                      evaluation_description))
