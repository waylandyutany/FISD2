from testing.testing_report import TestingReport, testing_report_class
from core.safe_utils import safe_path

################################################################################
@testing_report_class('.txt')
class TestingReport_TXT(TestingReport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.txt_lines = []
        self.txt_lines.append("TEST_REPORT('{}')".format(self.report_file_path))

        self.test_stat.enumerate(self)

        with open(safe_path(self.report_file_path), 'w') as f:
            for txt_line in self.txt_lines:
                print(txt_line)
                f.write(txt_line + "\n")
        

    def on_test_suite(self, test_suite_info):
        self.txt_lines.append("TEST_SUITE('{}')".format(test_suite_info.name))

    def on_test_set(self, test_set_info):
        self.txt_lines.append("    TEST_SET('{}')".format(test_set_info.name))

    def on_test_case(self, test_case_info):
        if test_case_info.failed_assertions > 0:
            self.txt_lines.append("        [FAIL]TEST_CASE('{}')".format(test_case_info.name))
        else:
            self.txt_lines.append("        [PASS]TEST_CASE('{}')".format(test_case_info.name))


