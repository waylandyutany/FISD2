from core.commands import command_class, Command

################################################################################
# TEST_SUITE Command
################################################################################
@command_class('test_suite')
class Test_suiteCommand(Command):
    _tag_test_suite = "#TEST_SUITE"
    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("{} '{}'...".format(cls._tag_test_suite, eargs.evaluated_args.value(0)))

################################################################################
# TEST_SET Command
################################################################################
@command_class('test_set')
class Test_setCommand(Command):
    _tag_test_set = "#TEST_SET"
    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("{} '{}'...".format(cls._tag_test_set, eargs.evaluated_args.value(0)))

################################################################################
# TEST_CASE Command
################################################################################
@command_class('test_case')
class Test_caseCommand(Command):
    _tag_test_case = "#TEST_CASE"
    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("{} '{}'...".format(cls._tag_test_case, eargs.evaluated_args.value(0)))

################################################################################
# TEST_ASSERT Command
################################################################################
@command_class('test_assert')
class Test_asserCommand(Command):
    _tag_passed = "#PASSED"
    _tag_failed = "#FAILED"

    @classmethod
    def execute(cls, eargs):
        if eargs.evaluated_args.value(0) == True:
            eargs.logger.info("{} '{}'".format(cls._tag_passed, 
                                               eargs.evaluated_args.value(1)))
        else:
            eargs.logger.warning("{} '{}', {}".format(cls._tag_failed, 
                                                      eargs.evaluated_args.eval_string(0),
                                                      eargs.evaluated_args.value(1)))

################################################################################
# TEST_RETURN_VALUE Command
################################################################################
@command_class('test_return_value')
class Test_return_valueCommand(Command):
    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("test_return_value({})".format(eargs.evaluated_args.value(0)))
        eargs.set_return(eargs.evaluated_args.value(0))
