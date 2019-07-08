import json
from core.safe_utils import safe_path

################################################################################
class TestingStatEnumerator:
    def __init__(self):
        self.test_suites = 0
        self.test_sets = 0
        self.test_cases = 0
        self.failed_test_cases = 0
        self.failed_assertions = 0
        self.passed_assertions = 0

    def on_test_suite(self, name, description):
        self.test_suites += 1

    def on_test_set(self, name, description):
        self.test_sets += 1

    def on_test_case(self, name, description, passed_assertions, failed_assertions):
        self.test_cases += 1
        self.failed_test_cases += 1 if failed_assertions > 0 else 0
        self.failed_assertions += failed_assertions
        self.passed_assertions += passed_assertions

################################################################################
class TestingStat:
    _key_test_suites = 'test_suites'
    _key_test_sets = 'test_sets'
    _key_test_cases = 'test_cases'
    _key_description = 'description'
    _key_passed = 'passed'
    _key_failed = 'failed'

    def __init__(self, logger):
        self.__logger = logger
        self.__suite_name = 'default_suite' #@todo or None instead ?
        self.__set_name = 'default_set'
        self.__tc_name = 'default_tc'
        self.__stat = {TestingStat._key_test_suites:{}}

    def save(self, file_path):
        j = json.dumps(self.__stat, indent=2)
        with open(safe_path(file_path), 'w') as f:
            f.write(j)

    def enumerate(self, testing_stat_enumerator):
        test_suites = self.__stat[TestingStat._key_test_suites]
        for suite_name in test_suites:
            testing_stat_enumerator.on_test_suite(suite_name, None)

            test_sets = test_suites[suite_name][TestingStat._key_test_sets]
            for set_name in test_sets:
                testing_stat_enumerator.on_test_set(set_name, None)

                test_cases = test_sets[set_name][TestingStat._key_test_cases]
                for tc_name in test_cases:
                    test_case = test_cases[tc_name]
                    testing_stat_enumerator.on_test_case(tc_name, None, test_case[TestingStat._key_passed], test_case[TestingStat._key_failed])

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
            return test_sets

        if set_name not in test_sets:
            test_sets[set_name] = {TestingStat._key_test_cases:{}}

        test_cases = test_sets[set_name][TestingStat._key_test_cases]

        if tc_name == None:
            return test_cases

        if self.__tc_name not in test_cases:
            test_cases[self.__tc_name] = {}
            TestingStat.__reset_tc_node(test_cases[self.__tc_name])

        return test_cases[self.__tc_name]

    @classmethod
    def __reset_tc_node(cls, tc_node):
        tc_node[cls._key_passed] = 0
        tc_node[cls._key_failed] = 0

    @classmethod
    def __increment_tc_node(cls, tc_node, passed, failed):
        tc_node[cls._key_passed] += passed
        tc_node[cls._key_failed] += failed

################################################################################
    def begin_test_suite(self, name, description):
        self.__suite_name = name
        node = self.__get_node(name)
        if description:
            node[TestingStat._key_description] = description

    def begin_test_set(self, name, description):
        self.__set_name = name
        node = self.__get_node(self.__suite_name, name)
        if description:
            node[TestingStat._key_description] = description

    def begin_test_case(self, name, description):
        self.__tc_name = name
        node = self.__get_node(self.__suite_name, self.__set_name, name)
        if description:
            node[TestingStat._key_description] = description
        TestingStat.__reset_tc_node(node)
        
    def check_assert(self, place, evaluation, evaluation_string, evaluation_description):
        node = self.__get_node(self.__suite_name, self.__set_name, self.__tc_name)
        passed = 1 if (evaluation == True) else 0
        failed = 1 if (evaluation == False) else 0
        TestingStat.__increment_tc_node(node, passed, failed)
