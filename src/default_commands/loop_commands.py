from core.commands import command_class, Command
from default_commands.keywords import Keywords
import core.code_utils as code_utils
from default_commands.default_commands import evaluate_string

################################################################################
#@todo move to token_utils
def search_keywords_in_tokens(tokens, keywords):
    ret = []
    for i in range(0, len(tokens)):
        for keyword in keywords:
            if tokens.is_keyword(i) and tokens.is_value_no_case(i, keyword):
                ret.append(i)
    return ret

def mark_tokens_as_keywords(tokens, keywords):
    for i in range(0, len(tokens)):
        if tokens.is_name(i):
            for keyword in keywords:
                if tokens.is_value_no_case(i, keyword):
                    tokens.mark_as_keyword(i)

def evaluate_tokens(tokens, start_index, end_index):
    str_to_evaluate = " ".join((tokens.value_str(i) for i in range(start_index + 1, end_index)))
    return evaluate_string(str_to_evaluate)

################################################################################
# FOR Command
################################################################################
@command_class(Keywords._FOR)
class ForCommand(Command):

    _keywords = [Keywords._FOR, Keywords._FROM, Keywords._TO, Keywords._STEP]

    @classmethod
    def parse_loop_tokens(cls, args):
        ''' return variable_name, from_value, to_value, step_value'''
        for_from_to_step_indicies = search_keywords_in_tokens(args, cls._keywords)
        variable_name = args.value(1)
        from_value = evaluate_tokens(args, for_from_to_step_indicies[1], for_from_to_step_indicies[2])
        to_value = evaluate_tokens(args, for_from_to_step_indicies[2], len(args))
        step_value = 1 #@todo evaluate step
        if args.is_number(7):
            step_value = args.value(7)

        return variable_name, from_value, to_value, step_value

    @classmethod
    def parse(cls, parse_args):
        _, line_tokens, _ = code_utils.split_code_line(parse_args.code_line)
        mark_tokens_as_keywords(line_tokens, cls._keywords)
        line_tokens.mark_as_keyword(1)

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
        nested_counter = 0
        for i in range(execute_args.code_index - 1, -1, -1):
            _, line_tokens, _ = code_utils.split_code_line(execute_args.code_lines[i])

            if line_tokens.is_value_no_case(0, Keywords._NEXT):
                nested_counter += 1

            if line_tokens.is_value_no_case(0, Keywords._FOR):
               if nested_counter == 0:
                    return i
               else:
                    nested_counter -= 1

        return None

    @classmethod
    def parse(cls, parse_args):
        _, line_tokens, _ = code_utils.split_code_line(parse_args.code_line)
        line_tokens.mark_as_keyword(1)

    @classmethod
    def execute(cls, execute_args):
        #@todo handle nested loops within search function
        #@todo handle from > to
        #@todo check next name with it's for name
        loop_start_index = cls.search_for_loop_start(execute_args)
        _, line_tokens, _ = code_utils.split_code_line(execute_args.code_lines[loop_start_index])
        variable_name, from_value, to_value, step_value = ForCommand.parse_loop_tokens(line_tokens)
        value = execute_args.context.get_variable(variable_name)
        value = value + step_value
        execute_args.context.set_variable(variable_name, value)
        if value < to_value:
            execute_args.context.jump_to_code(loop_start_index + 1)

