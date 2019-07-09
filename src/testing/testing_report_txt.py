from testing.testing_report import TestingReport, testing_report_class

################################################################################
@testing_report_class('.txt')
class TestingReport_TXT(TestingReport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_stat.enumerate(self)

    def on_test_suite(self, name, description):
        print("on_test_suite")
        pass

    def on_test_set(self, name, description):
        print("on_test_set")
        pass

    def on_test_case(self, name, description, passed_assertions, failed_assertions):
        print("on_test_case")
        pass


