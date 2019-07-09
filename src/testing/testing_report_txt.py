from testing.testing_report import TestingReport, testing_report_class

################################################################################
@testing_report_class('.txt')
class TestingReport_TXT(TestingReport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_stat.enumerate(self)

    def on_test_suite(self, test_suite_info):
        print("on_test_suite : ", test_suite_info.name)

    def on_test_set(self, test_set_info):
        print("on_test_set : ", test_set_info.name)

    def on_test_case(self, test_case_info):
        print("on_test_case : ", test_case_info.name)


