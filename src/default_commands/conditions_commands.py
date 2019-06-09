from core.commands import command_class, Command
from default_commands.keywords import Keywords
from core.code_line import Code_line

################################################################################
# IF Command
################################################################################
@command_class(Keywords._IF)
class IfCommand(Command):
    _KEY_NEXT_CONDITION_CODE_INDEX = 'next_condition_code_index'
    _KEY_END_CONDITION_CODE_INDEX = 'end_condition_code_index'

    _keywords = [Keywords._THEN]

    @classmethod
    def search_for_if_commands(cls, code_lines, code_index):
        ''' Returns code indicies for all if conditional commands (if, elif, else, endif)'''
        ret = []
        nested_counter = 0
        ret.append(code_index)
        for i in range(code_index + 1, len(code_lines)):
            _, line_tokens, _ = Code_line.split(code_lines[i])

            if line_tokens.is_value_no_case(0, Keywords._IF):
                nested_counter += 1

            if line_tokens.is_value_no_case(0, Keywords._END_IF):
               if nested_counter == 0:
                    ret.append(i)
                    return ret
               else:
                    nested_counter -= 1

            if nested_counter == 0:
                if line_tokens.is_value_no_case(0, [Keywords._ELSE, Keywords._ELIF]):
                    ret.append(i)

        return ret

    @classmethod
    def parse(cls, parse_args):
        #@todo error when no correct order if, elif..., else, endif
        #@todo error when no endif
        if_commands = cls.search_for_if_commands(parse_args.code_lines, parse_args.code_index)

        #set _KEY_NEXT_CONDITION_CODE_INDEX for all conditional commands, except endif
        for i in range(0, len(if_commands) - 1):
            code_index = if_commands[i]

            next_condition_code_index = if_commands[i + 1]
            end_condition_code_index = if_commands[-1]

            _, line_tokens, _ = Code_line.split(parse_args.code_lines[code_index])

            parse_args.code_lines[code_index][IfCommand._KEY_NEXT_CONDITION_CODE_INDEX] = next_condition_code_index
    
            # _KEY_END_CONDITION_CODE_INDEX optimization apply only for elseif statement
            if line_tokens.is_value_no_case(0, Keywords._ELIF):
                parse_args.code_lines[code_index][IfCommand._KEY_END_CONDITION_CODE_INDEX] = end_condition_code_index
        
    @classmethod
    def execute_if(cls, execute_args):
        result = execute_args.arguments.evaluate_tokens(0, len(execute_args.arguments) - 1)

        if result and (not execute_args.context.is_skip_if()):
            execute_args.context.skip_if()
        else:
            next_condition_code_index = execute_args.code_line[IfCommand._KEY_NEXT_CONDITION_CODE_INDEX]
            execute_args.context.jump_to_code(next_condition_code_index)

    @classmethod
    def execute(cls, execute_args):
        # must be first !!!
        execute_args.context.begin_if()

        cls.execute_if(execute_args)

################################################################################
# ENDIF Command
################################################################################
@command_class(Keywords._END_IF)
class EndIfProcCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        execute_args.context.end_if()

################################################################################
# ELSE Command
################################################################################
@command_class(Keywords._ELSE)
class ElseProcCommand(Command):
    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        if execute_args.context.is_skip_if():
            next_condition_code_index = execute_args.code_line[IfCommand._KEY_NEXT_CONDITION_CODE_INDEX]
            execute_args.context.jump_to_code(next_condition_code_index)

################################################################################
# ELIF Command
################################################################################
@command_class(Keywords._ELIF)
class ElifProcCommand(Command):
    _keywords = [Keywords._THEN]

    @classmethod
    def parse(cls, parse_args):
        pass

    @classmethod
    def execute(cls, execute_args):
        # jump to the if end when condition already satisfied, preventing condition statement evaluation
        if execute_args.context.is_skip_if():
            end_condition_code_index = execute_args.code_line[IfCommand._KEY_END_CONDITION_CODE_INDEX]
            execute_args.context.jump_to_code(end_condition_code_index)
            return

        IfCommand.execute_if(execute_args)
