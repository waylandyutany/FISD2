from core.commands.commands import command_class, Command
from core.code.code_line import Code_line

################################################################################
# FOR Command
################################################################################
@command_class()
class ForCommand(Command):
    _FOR = 'for'
    _FROM = 'from'
    _TO = 'to'
    _STEP = 'step'
    _NEXT = 'next'

    _keyword = _FOR
    _keywords = [_FOR, _FROM, _TO, _STEP]

    @classmethod
    def search_for_loop_end(cls, code_lines, code_index):
        nested_counter = 0
        for i in range(code_index + 1, len(code_lines)):
            _, line_tokens, _ = Code_line.split(code_lines[i])

            if line_tokens.is_value_no_case(0, cls._FOR):
                nested_counter += 1

            if line_tokens.is_value_no_case(0, cls._NEXT):
               if nested_counter == 0:
                    return i
               else:
                    nested_counter -= 1

        return None #hen no next found!

    @classmethod
    def evaluate_for_tokens(cls, args):
        ''' return variable_name, from_value, to_value, step_value'''
        for_from_to_step_indicies = args.search_keywords_in_tokens(cls._keywords)
        variable_name = args.value(1)
        from_value = args.evaluate_tokens(for_from_to_step_indicies[1], for_from_to_step_indicies[2])

        try:
            to_value = args.evaluate_tokens(for_from_to_step_indicies[2], for_from_to_step_indicies[3])
            step_value = args.evaluate_tokens(for_from_to_step_indicies[3], len(args))
        except:
            to_value = args.evaluate_tokens(for_from_to_step_indicies[2], len(args))
            step_value = 1 if from_value <= to_value else -1

        return variable_name, from_value, to_value, step_value

    @classmethod
    def parse(cls, pargs):
        _, line_tokens, _ = Code_line.split(pargs.code_line)
        line_tokens.mark_as_keyword(1)

        #@todo error if wrong arguments

        #detecting loop end and set jump code index for next and for commands into their code_lines
        for_code_index = pargs.code_index
        next_code_index = cls.search_for_loop_end(pargs.code_lines, pargs.code_index)
        if not next_code_index:
            #@todo error no loop ending 
            #@todo error when variable name is not the same for for and next
            #@todo warning if no variable name behind next
            pass
        else:
            for_label_name = pargs.code_labels.get_label_name(cls._FOR)
            next_label_name = pargs.code_labels.get_label_name(cls._NEXT)

            Code_line.add_label(pargs.code_lines[for_code_index], for_label_name)
            Code_line.add_label(pargs.code_lines[next_code_index], next_label_name)

            Code_line.add_jump(pargs.code_lines[for_code_index], cls._NEXT, next_label_name)
            Code_line.add_jump(pargs.code_lines[next_code_index], cls._FOR, for_label_name)

    @classmethod
    def execute(cls, eargs):
        variable_name, from_value, to_value, step_value = cls.evaluate_for_tokens(eargs.raw_args)
        eargs.context.set_variable(variable_name, from_value)
        next_code_index = Code_line.get_jump(eargs.code_line, cls._NEXT)
        #@todo handle if value is already over to _value
        #@todo handle if from > to
        #@todo handle other then number values (e.g. dates)

################################################################################
# NEXT Command
################################################################################
@command_class(ForCommand._NEXT)
class NextProcCommand(Command):
    @classmethod
    def parse(cls, pargs):
        _, line_tokens, _ = Code_line.split(pargs.code_line)
        line_tokens.mark_as_keyword(1)

    @classmethod
    def execute(cls, eargs):
        #@todo one time warning if infinite loop detected
        for_code_index = Code_line.get_jump(eargs.code_line, ForCommand._FOR)
        _, line_tokens, _ = Code_line.split(eargs.code_lines[for_code_index])
        variable_name, from_value, to_value, step_value = ForCommand.evaluate_for_tokens(line_tokens)
        value = eargs.context.get_variable(variable_name)
        value = value + step_value
        eargs.context.set_variable(variable_name, value)

        if from_value < to_value:
            if value < to_value:
                eargs.context.jump_to_code(for_code_index + 1)
        else:
            if value > to_value:
                eargs.context.jump_to_code(for_code_index + 1)

