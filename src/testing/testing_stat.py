import json
from core.safe_utils import safe_path
from testing.testing_stat_enumerators import TestCaseEnumerator

################################################################################
class TestSuiteInfo:
    def __init__(self, name, suite_node):
        self.name = name
        self.description = suite_node[TestingStat._key_description] if TestingStat._key_description in suite_node else None

class TestSetInfo:
    def __init__(self, name, set_node):
        self.name = name
        self.description = set_node[TestingStat._key_description] if TestingStat._key_description in set_node else None

class TestCaseInfo:
    def __init__(self, name, case_node):
        self.name = name
        self.description = case_node[TestingStat._key_description] if TestingStat._key_description in case_node else None

        self.passed_assertions = case_node[TestingStat._key_passed]
        self.failed_assertions = case_node[TestingStat._key_failed]
        self.failures = []
        if TestingStat._key_failures in case_node:
            for failure in case_node[TestingStat._key_failures]:
                self.failures.append(FailureInfo(failure[TestingStat._key_what],
                                                 failure[TestingStat._key_why],
                                                 failure[TestingStat._key_where]))

class FailureInfo:
    def __init__(self, what, why, where):
        self.what = what
        self.why = why
        self.where = where

################################################################################
class TestingStat:
    _key_test_suites = 'test_suites'
    _key_test_sets = 'test_sets'
    _key_test_cases = 'test_cases'
    _key_description = 'description'
    _key_passed = 'passed'
    _key_failed = 'failed'
    _key_test_suite = 'test_suite'
    _key_test_set = 'test_set'
    _key_test_case = 'test_case'
    _key_default = 'default'
    _key_failures = 'failures'
    _key_where = 'where'
    _key_why = 'why'
    _key_what = 'what'

    def __init__(self, logger):
        self.__logger = logger
        self.__stat = {TestingStat._key_test_suites:{}}

    def save(self, file_path):
        j = json.dumps(self.__stat, indent=2)
        with open(safe_path(file_path), 'w') as f:
            f.write(j)

    def enumerate(self, testing_stat_enumerator):
        test_suites = self.__stat[TestingStat._key_test_suites]
        for suite_name in test_suites:
            if hasattr(testing_stat_enumerator,'on_test_suite'):
                testing_stat_enumerator.on_test_suite(TestSuiteInfo(suite_name,test_suites[suite_name]))

            test_sets = test_suites[suite_name][TestingStat._key_test_sets]
            for set_name in test_sets:
                if hasattr(testing_stat_enumerator,'on_test_set'):
                    testing_stat_enumerator.on_test_set(TestSetInfo(set_name, test_sets[set_name]))

                test_cases = test_sets[set_name][TestingStat._key_test_cases]
                for tc_name in test_cases:
                    test_case = test_cases[tc_name]
                    if hasattr(testing_stat_enumerator,'on_test_case'):
                        testing_stat_enumerator.on_test_case(TestCaseInfo(tc_name, test_case))

################################################################################
    @property
    def logger(self):
        return self.__logger

################################################################################
    def __get_node(self, suite_name, set_name = None, tc_name = None):
        test_suites = self.__stat[TestingStat._key_test_suites]

        if suite_name not in test_suites:
            test_suites[suite_name] = {TestingStat._key_test_sets:{}}

        test_sets = test_suites[suite_name][TestingStat._key_test_sets]

        if set_name == None:
            return test_suites[suite_name]

        if set_name not in test_sets:
            test_sets[set_name] = {TestingStat._key_test_cases:{}}

        test_cases = test_sets[set_name][TestingStat._key_test_cases]

        if tc_name == None:
            return test_sets[set_name]

        if tc_name not in test_cases:
            test_cases[tc_name] = {}
            TestingStat.__reset_tc_node(test_cases[tc_name])

        return test_cases[tc_name]

    @classmethod
    def __reset_tc_node(cls, tc_node):
        tc_node[cls._key_passed] = 0
        tc_node[cls._key_failed] = 0

    @classmethod
    def __increment_tc_node(cls, tc_node, passed, failed):
        tc_node[cls._key_passed] += passed
        tc_node[cls._key_failed] += failed

    @classmethod
    def __add_failure(cls, tc_node, place, evaluation_string, evaluation_description):
        if cls._key_failures not in tc_node:
            tc_node[cls._key_failures] = []
        tc_node[cls._key_failures].append({ cls._key_where:place,
                                            cls._key_why : evaluation_string,
                                            cls._key_what : evaluation_description })

################################################################################
    def begin_test_suite(self, system_var, name, description):
        system_var.set(TestingStat._key_test_suite, name)
        node = self.__get_node(name)
        node[TestingStat._key_description] = description

    def begin_test_set(self, system_var, name, description):
        system_var.set(TestingStat._key_test_set, name)
        node = self.__get_node(system_var.get(TestingStat._key_test_suite, TestingStat._key_default),
                               name)
        node[TestingStat._key_description] = description

    def begin_test_case(self, system_var, name, description):
        system_var.set(TestingStat._key_test_case, name)
        node = self.__get_node(system_var.get(TestingStat._key_test_suite, TestingStat._key_default),
                               system_var.get(TestingStat._key_test_set, TestingStat._key_default),
                               name)
        node[TestingStat._key_description] = description
        TestingStat.__reset_tc_node(node)
        
    def check_assert(self, system_var, place, evaluation, evaluation_string, evaluation_description):
        node = self.__get_node(system_var.get(TestingStat._key_test_suite, TestingStat._key_default),
                               system_var.get(TestingStat._key_test_set, TestingStat._key_default),
                               system_var.get(TestingStat._key_test_case, TestingStat._key_default))
        passed = 1 if (evaluation == True) else 0
        failed = 1 if (evaluation == False) else 0
        TestingStat.__increment_tc_node(node, passed, failed)

        if (evaluation == False):
            TestingStat.__add_failure(node, place, evaluation_string, evaluation_description)

    def test_case_passed_assertions(self, system_var, tc_name):
        ts_test_case = TestCaseEnumerator(tc_name if tc_name else system_var.get(TestingStat._key_test_case))
        self.enumerate(ts_test_case)
        return ts_test_case.passed_assertions

    def test_case_failed_assertions(self, system_var, tc_name):
        ts_test_case = TestCaseEnumerator(tc_name if tc_name else system_var.get(TestingStat._key_test_case))
        self.enumerate(ts_test_case)
        return ts_test_case.failed_assertions
