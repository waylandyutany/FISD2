################################################################################
class TestingStatEnumerator:
    def on_test_suite(self, test_suite_info):
        pass

    def on_test_set(self, test_set_info):
        pass

    def on_test_case(self, test_case_info):
        pass

################################################################################
class TestCounterEnumerator:
    def __init__(self):
        self.test_suites = 0
        self.test_sets = 0
        self.test_cases = 0
        self.failed_test_cases = 0
        self.failed_assertions = 0
        self.passed_assertions = 0

    def on_test_suite(self, test_suite_info):
        self.test_suites += 1

    def on_test_set(self, test_set_info):
        self.test_sets += 1

    def on_test_case(self, test_case_info):
        self.test_cases += 1
        self.failed_test_cases += 1 if test_case_info.failed_assertions > 0 else 0
        self.failed_assertions += test_case_info.failed_assertions
        self.passed_assertions += test_case_info.passed_assertions

################################################################################
class TestCasesEnumerator:
    def __init__(self):
        self.test_cases = 0
        self.failed_test_cases = 0

    def on_test_case(self, test_case_info):
        self.test_cases += 1
        self.failed_test_cases += 1 if test_case_info.failed_assertions > 0 else 0

################################################################################
class TestCaseEnumerator:
    def __init__(self, name):
        self.failed_assertions = None
        self.passed_assertions = None
        self.__name = name.lower()

    def on_test_case(self, test_case_info):
        if test_case_info.name.lower() == self.__name:
            self.failed_assertions = test_case_info.failed_assertions
            self.passed_assertions = test_case_info.passed_assertions

