from core.commands import command_class, Command
from core.command_type import CallableCommand as Callable
from testing.testing import Testing

################################################################################
# TEST_SUITE Command
################################################################################
@command_class('test_suite')
class Test_suiteCommand(Command):
    @classmethod
    def execute(cls, params):
        eargs = params.evaluated_args
        Testing.begin_test_suite(eargs.value(0), eargs.value(1))

################################################################################
# TEST_SET Command
################################################################################
@command_class('test_set')
class Test_setCommand(Command):
    @classmethod
    def execute(cls, params):
        eargs = params.evaluated_args
        Testing.begin_test_set(eargs.value(0), eargs.value(1))

################################################################################
# TEST_CASE Command
################################################################################
@command_class('test_case')
class Test_caseCommand(Command):
    @classmethod
    def execute(cls, params):
        eargs = params.evaluated_args
        Testing.begin_test_case(eargs.value(0), eargs.value(1))

################################################################################
# TEST_ASSERT Command
################################################################################
@command_class('test_assert')
class Test_asserCommand(Command):
    _tag_passed = "#PASSED"
    _tag_failed = "#FAILED"

    @classmethod
    def execute(cls, params):
        eargs = params.evaluated_args
        if eargs.value(0) == True:
            params.logger.info("{} '{}'".format(cls._tag_passed, 
                                               eargs.value(1)))
        else:
            params.logger.warning("{} '{}', {}".format(cls._tag_failed, 
                                                      eargs.eval_string(0),
                                                      eargs.value(1)))

################################################################################
# TEST_RETURN_VALUE Command
################################################################################
@command_class('test_return_value', Callable())
class Test_return_valueCommand(Command):
    @classmethod
    def execute(cls, eargs):
        eargs.set_return(eargs.evaluated_args.value(0))
