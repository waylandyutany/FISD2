import json

################################################################################
class TestingStat:
    _key_test_suites = 'test_suites'
    _key_test_sets = 'test_sets'
    _key_test_cases = 'test_cases'
    _key_description = 'description'

    def __init__(self, logger):
        self.__logger = logger
        self.__suite_name = 'default_suite'
        self.__set_name = 'default_set'
        self.__tc_name = 'default_tc'
        self.__stat = {TestingStat._key_test_suites:{}}

    def save(self, file_path):
        j = json.dumps(self.__stat, indent=2)
        with open(file_path, 'w') as f:
            f.write(j)

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

        return test_cases[self.__tc_name]

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
        
    def check_assert(self, place, evaluation, evaluation_string, evaluation_description):
        pass