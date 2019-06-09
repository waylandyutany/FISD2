from core.commands import command_class, Command
from default_commands.keywords import Keywords
import core.code_utils as code_utils
from core.code_line import Code_line

################################################################################
# FOR Command
################################################################################
@command_class(Keywords._FOR)
class ForCommand(Command):
    _keywords = [Keywords._FOR, Keywords._FROM, Keywords._TO, Keywords._STEP]

    @classmethod
    def search_for_loop_end(cls, code_lines, code_index):
        nested_counter = 0
        for i in range(code_index + 1, len(code_lines)):
            _, line_tokens, _ = Code_line.split_code_line(code_lines[i])

            if line_tokens.is_value_no_case(0, Keywords._FOR):
                nested_counter += 1

            if line_tokens.is_value_no_case(0, Keywords._NEXT):
               if nested_counter == 0:
                    return i
               else:
                    nested_counter -= 1

        return None

    @classmethod
    def evaluate_for_tokens(cls, args):
        ''' return variable_name, from_value, to_value, step_value'''
        for_from_to_step_indicies = args.search_keywords_in_tokens(cls._keywords)
        variable_name = args.value(1)
        from_value = code_utils.evaluate_tokens(args, for_from_to_step_indicies[1], for_from_to_step_indicies[2])

        try:
            to_value = code_utils.evaluate_tokens(args, for_from_to_step_indicies[2], for_from_to_step_indicies[3])
            step_value = code_utils.evaluate_tokens(args, for_from_to_step_indicies[3], len(args))
        except:
            to_value = code_utils.evaluate_tokens(args, for_from_to_step_indicies[2], len(args))
            step_value = 1 if from_value <= to_value else -1

        return variable_name, from_value, to_value, step_value

    @classmethod
    def parse(cls, parse_args):
        _, line_tokens, _ = Code_line.split_code_line(parse_args.code_line)
        line_tokens.mark_as_keyword(1)

        #@todo error if wrong arguments

        #detecting loop end and set jump code index for next and for commands into their code_lines
        for_code_index = parse_args.code_index
        next_code_index = cls.search_for_loop_end(parse_args.code_lines, parse_args.code_index)
        if not next_code_index:
            #@todo error no loop ending 
            #@todo error when variable name is not the same for for and next
            #@todo warning if no variable name behind next
            pass
        else:
            for_label_name = parse_args.code_labels.get_label_name(Keywords._FOR)
            next_label_name = parse_args.code_labels.get_label_name(Keywords._NEXT)

            Code_line.add_code_line_label(parse_args.code_lines[for_code_index], for_label_name)
            Code_line.add_code_line_label(parse_args.code_lines[next_code_index], next_label_name)

            Code_line.add_code_line_jump(parse_args.code_lines[for_code_index], Keywords._NEXT, next_label_name)
            Code_line.add_code_line_jump(parse_args.code_lines[next_code_index], Keywords._FOR, for_label_name)

    @classmethod
    def execute(cls, execute_args):
        variable_name, from_value, to_value, step_value = cls.evaluate_for_tokens(execute_args.arguments)
        execute_args.context.set_variable(variable_name, from_value)
        next_code_index = Code_line.get_code_line_jump(execute_args.code_line, Keywords._NEXT)
        #@todo handle if value is already over to _value
        #@todo handle if from > to
        #@todo handle other then number values (e.g. dates)

################################################################################
# NEXT Command
################################################################################
@command_class(Keywords._NEXT)
class NextProcCommand(Command):

    @classmethod
    def parse(cls, parse_args):
        _, line_tokens, _ = Code_line.split_code_line(parse_args.code_line)
        line_tokens.mark_as_keyword(1)

    @classmethod
    def execute(cls, execute_args):
        #@todo one time warning if infinite loop detected
        for_code_index = Code_line.get_code_line_jump(execute_args.code_line, Keywords._FOR)
        _, line_tokens, _ = Code_line.split_code_line(execute_args.code_lines[for_code_index])
        variable_name, from_value, to_value, step_value = ForCommand.evaluate_for_tokens(line_tokens)
        value = execute_args.context.get_variable(variable_name)
        value = value + step_value
        execute_args.context.set_variable(variable_name, value)

        if from_value < to_value:
            if value < to_value:
                execute_args.context.jump_to_code(for_code_index + 1)
        else:
            if value > to_value:
                execute_args.context.jump_to_code(for_code_index + 1)

