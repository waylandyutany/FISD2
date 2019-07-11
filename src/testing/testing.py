from testing.testing_stat import TestingStat
from testing.testing_stat_enumerators import TestCounterEnumerator, TestCasesEnumerator
from testing.testing_report import TestingReport
import testing.testing_report_txt
import os

#@todo warning if same test case begin
################################################################################
class Testing:
    _tag_test_suite = "#TEST_SUITE"
    _tag_test_set = "#TEST_SET"
    _tag_test_case = "#TEST_CASE"
    _tag_passed = "#PASSED"
    _tag_failed = "#FAILED"

    __stat = None
    __logger = None
    __report_file = None
    __test_cases = {}

    @classmethod
    def init(cls, report_file, merge_report_file, logger):
        cls.__stat = TestingStat(logger)
        cls.__logger = logger
        cls.__report_file = report_file
         
        cls.__report_class = None

        if cls.__report_file:
            cls.__stat_file = report_file + ".json"
            _, report_extension = os.path.splitext(cls.__report_file)
            cls.__report_class = TestingReport.find_report_class(report_extension)
            if not cls.__report_class:
                cls.__logger.error("Unable to find '{}' report class!".format(report_extension))
        
            if merge_report_file and os.path.isfile(cls.__stat_file):
                cls.__logger.info("Merging report file '{}'...".format(cls.__stat_file))
                cls.__stat.load_from_file(cls.__stat_file)

    @classmethod
    def log_stat(cls):
        ts_counter = TestCounterEnumerator()
        cls.__stat.enumerate(ts_counter)
        cls.__logger.info("Testing statistics :".format())
        cls.__logger.info("Total Test Suites({}), Sets({}), Cases({}), Failed cases({})".format(ts_counter.test_suites,
                                                                                                ts_counter.test_sets, 
                                                                                                ts_counter.test_cases,
                                                                                                ts_counter.failed_test_cases))
        cls.__logger.info("Total Assertions({}), Failed Assertions({}), Passed Assertions({})".format(ts_counter.failed_assertions + ts_counter.passed_assertions,
                                                                                                      ts_counter.failed_assertions,
                                                                                                      ts_counter.passed_assertions))
#        cls.__logger.info("".format())

    @classmethod
    def finalize(cls):
        cls.log_stat()

        if cls.__report_file:
            cls.__stat.save_to_file(cls.__stat_file)

        if cls.__report_class:
            report = cls.__report_class(cls.__logger, cls.__report_file, cls.__stat)

    @classmethod
    def begin_test_suite(cls, system_var, name, description):
        cls.__logger.info("{} '{}'...".format(cls._tag_test_suite, name))
        cls.__stat.begin_test_suite(system_var, 
                                    name, 
                                    description)

    @classmethod
    def begin_test_set(cls, system_var, name, description):
        cls.__logger.info("{} '{}'...".format(cls._tag_test_set, name))
        cls.__stat.begin_test_set(system_var, 
                                  name, 
                                  description)

    @classmethod
    def begin_test_case(cls, system_var, where, name, description):
        #@todo test case for this, warning if test_case with same name on different place
        lower_name = name.lower()
        if lower_name in cls.__test_cases and cls.__test_cases[lower_name] != where:
            cls.__logger.warning("Test case '{}' already defined here '{}'!".format(name, cls.__test_cases[lower_name]))
        cls.__test_cases[lower_name] = where


        cls.__logger.info("{} '{}'...".format(cls._tag_test_case, name))
        cls.__stat.begin_test_case(system_var, 
                                   name, 
                                   description)

    @classmethod
    def test_assert(cls, system_var, evaluation, evaluation_string, evaluation_description):
        cls.__stat.check_assert(system_var,
                                cls.__logger.preface, 
                                evaluation, 
                                evaluation_string, 
                                evaluation_description)

        if evaluation == True:
            cls.__logger.info("{} '{}'".format(cls._tag_passed, 
                                               evaluation_description))
        else:
            cls.__logger.warning("{} '{}', {}".format(cls._tag_failed, 
                                                      evaluation_string,
                                                      evaluation_description))

    @classmethod
    def test_cases_total(cls):
        ts_test_cases = TestCasesEnumerator()
        cls.__stat.enumerate(ts_test_cases)
        return ts_test_cases.test_cases

    @classmethod
    def test_cases_passed(cls):
        ts_test_cases = TestCasesEnumerator()
        cls.__stat.enumerate(ts_test_cases)
        return ts_test_cases.test_cases - ts_test_cases.failed_test_cases


    @classmethod
    def test_case_passed_assertions(cls, system_var, tc_name):
        ts_test_case = TestingStatTestCase(tc_name if tc_name else system_var.get('TestingStat._key_test_case'))
        return ts_test_case.passed_assertions

    @classmethod
    def test_case_failed_assertions(cls, system_var, tc_name):
        ts_test_case = TestingStatTestCase(tc_name if tc_name else system_var.get('TestingStat._key_test_case'))
        return ts_test_case.failed_assertions

    @classmethod
    def test_case_passed_assertions(cls, system_var, tc_name):
        return cls.__stat.test_case_passed_assertions(system_var, tc_name)

    @classmethod
    def test_case_failed_assertions(cls, system_var, tc_name):
        return cls.__stat.test_case_failed_assertions(system_var, tc_name)
