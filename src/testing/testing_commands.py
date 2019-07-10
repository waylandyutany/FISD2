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
        system_var = params.context.system_variables
        Testing.begin_test_suite(system_var, eargs.value(0), eargs.value(1))

################################################################################
# TEST_SET Command
################################################################################
@command_class('test_set')
class Test_setCommand(Command):
    @classmethod
    def execute(cls, params):
        eargs = params.evaluated_args
        system_var = params.context.system_variables
        Testing.begin_test_set(system_var, eargs.value(0), eargs.value(1))

################################################################################
# TEST_CASE Command
################################################################################
@command_class('test_case')
class Test_caseCommand(Command):
    @classmethod
    def execute(cls, params):
        eargs = params.evaluated_args
        system_var = params.context.system_variables
        where = params.logger.preface
        Testing.begin_test_case(system_var, where, eargs.value(0), eargs.value(1))

################################################################################
# TEST_ASSERT Command
################################################################################
@command_class('test_assert')
class Test_asserCommand(Command):
    @classmethod
    def execute(cls, params):
        eargs = params.evaluated_args
        system_var = params.context.system_variables
        Testing.test_assert(system_var, 
                            evaluation = eargs.value(0),
                            evaluation_string=eargs.eval_string(0),
                            evaluation_description = eargs.value(1))

################################################################################
# TEST_RETURN_VALUE Command
################################################################################
@command_class('test_return_value', Callable())
class Test_return_valueCommand(Command):
    @classmethod
    def execute(cls, params):
        params.set_return(params.evaluated_args.value(0))

################################################################################
# TEST_CASES_TOTAL Command
################################################################################
@command_class('test_cases_total')
class Test_cases_totalCommand(Command):
    @classmethod
    def execute(cls, params):
        pass

################################################################################
# TEST_CASES_PASSED Command
################################################################################
@command_class('test_cases_passed')
class Test_cases_passedCommand(Command):
    @classmethod
    def execute(cls, params):
        pass

################################################################################
# TEST_CASE_PASSED Command
################################################################################
@command_class('test_case_passed')
class Test_case_passedCommand(Command):
    @classmethod
    def execute(cls, params):
        pass

