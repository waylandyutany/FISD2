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
        eargs.logger.info("Begin test suite '{}'...".format(eargs.args.value(0)))

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
        eargs.logger.info("Begin test set '{}'...".format(eargs.args.value(0)))

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
        eargs.logger.info("Begin test case '{}'...".format(eargs.args.value(0)))

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
        if eargs.args.value(0) == True:
            eargs.logger.info("PASSED '{}', '{}'".format(eargs.args.eval_string(0), eargs.args.value(1)))
        else:
            eargs.logger.error("FAILED '{}', {}".format(eargs.args.eval_string(0), eargs.args.value(1)))

