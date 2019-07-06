from testing.testing_stat import TestingStat

################################################################################
class Testing:
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
        cls.__stat.begin_test_suite(name, description)

    @classmethod
    def begin_test_set(cls, name, description):
        cls.__stat.begin_test_set(name, description)

    @classmethod
    def begin_test_case(cls, name, description):
        cls.__stat.begin_test_case(name, description)
