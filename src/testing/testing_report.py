################################################################################
class TestingReport:
    _report_classes = {}

    @classmethod
    def find_report_class(cls, extension):
        extension = extension.lower()
        if extension in cls._report_classes:
            return cls._report_classes[extension]
        return None

    def __init__(self, logger, report_file_path, test_stat):
        self.__logger = logger
        self.__report_file_path = report_file_path
        self.__test_stat = test_stat

    @property
    def logger(self):
        return self.__logger

    @property
    def report_file_path(self):
        return self.__report_file_path

    @property
    def test_stat(self):
        return self.__test_stat

################################################################################
def testing_report_class(extension):
    def _testing_report_class(report_class):
        TestingReport._report_classes[extension.lower()] = report_class
        return report_class
    return _testing_report_class


