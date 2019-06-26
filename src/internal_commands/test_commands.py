from core.commands import command_class, Command

################################################################################
# TEST_SUITE Command
################################################################################
@command_class()
class Test_suiteCommand(Command):
    _keyword = 'test_suite'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("{}({})".format(cls._keyword, str(eargs)))

################################################################################
# TEST_SET Command
################################################################################
@command_class()
class Test_setCommand(Command):
    _keyword = 'test_set'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("{}({})".format(cls._keyword, str(eargs)))

################################################################################
# TEST_CASE Command
################################################################################
@command_class()
class Test_caseCommand(Command):
    _keyword = 'test_case'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("{}({})".format(cls._keyword, str(eargs)))

################################################################################
# TEST_ASSERT Command
################################################################################
@command_class()
class Test_asserCommand(Command):
    _keyword = 'test_assert'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("{}({})".format(cls._keyword, str(eargs)))

