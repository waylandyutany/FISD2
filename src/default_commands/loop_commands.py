from core.commands import command_class, Command
from default_commands.keywords import Keywords
import core.code_utils as code_utils

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

        #@todo handle if value is already over to _value
        #@todo handle is from > to
        #@todo handle other then number values (e.g. dates)

################################################################################
# NEXT Command
################################################################################
@command_class(Keywords._NEXT)
class NextProcCommand(Command):

    @classmethod
    def search_for_loop_start(cls, execute_args):
        for i in range(execute_args.code_index, 0, -1):
            _, line_tokens, _ = code_utils.split_code_line(execute_args.code_lines[i])
            if line_tokens.is_value_no_case(0, Keywords._FOR):
                return i
        return None

    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        #@todo handle nested loops within search function
        #@todo handle from > to
        loop_start_index = cls.search_for_loop_start(execute_args)
        _, line_tokens, _ = code_utils.split_code_line(execute_args.code_lines[loop_start_index])
        variable_name, from_value, to_value, step_value = ForCommand.parse_loop_tokens(line_tokens)
        value = execute_args.context.get_variable(variable_name)
        value = value + step_value
        execute_args.context.set_variable(variable_name, value)
        if value < to_value:
            execute_args.context.jump_to_code(loop_start_index + 1)

