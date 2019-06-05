from core.commands import command_class, Command
from default_commands.keywords import Keywords

################################################################################
# FOR Command
################################################################################
@command_class(Keywords._FOR)
class ForCommand(Command):

    @classmethod
    def parse_loop_tokens(cls, args):
        ''' return variable_name, from_value, to_value, step_value'''
        variable_name = args.value(1)
        from_value = args.value(3)
        to_value = args.value(5)
        step_value = 1
        if args.is_number(7):
            step_value = args.value(7)

        return variable_name, from_value, to_value, step_value

    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        variable_name, from_value, to_value, step_value = cls.parse_loop_tokens(execute_args.arguments)
        execute_args.context.set_variable(variable_name, from_value)
        pass
        #@todo handle if value is already over to _value
        #@todo handle is from > to
        #@todo handle other then number values (e.g. dates)
################################################################################
# NEXT Command
################################################################################
@command_class(Keywords._NEXT)
class NextProcCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        pass

