################################################################################
class TestingStatEnumerator:
    def on_test_suite(self, test_suite_info):
        pass

    def on_test_set(self, test_set_info):
        pass

    def on_test_case(self, test_case_info):
        pass

################################################################################
class TestingStatCounter:
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
class TestingStatTestCases:
    def __init__(self):
        self.test_cases = 0
        self.failed_test_cases = 0

    def on_test_case(self, test_case_info):
        self.test_cases += 1
        self.failed_test_cases += 1 if test_case_info.failed_assertions > 0 else 0
