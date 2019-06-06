from core.commands import command_class, Command
from default_commands.keywords import Keywords
import core.code_utils as code_utils

################################################################################
# IF Command
################################################################################
@command_class(Keywords._IF)
class IfCommand(Command):

    _keywords = [Keywords._THEN]

    @classmethod
    def search_for_if_statements(cls, code_lines, code_index):
        ret = []
        nested_counter = 0
        for i in range(code_index + 1, len(code_lines)):
            _, line_tokens, _ = code_utils.split_code_line(code_lines[i])

            if line_tokens.is_value_no_case(0, Keywords._IF):
                nested_counter += 1

            if line_tokens.is_value_no_case(0, Keywords._END_IF):
               if nested_counter == 0:
                    ret.append(i)
                    return ret
               else:
                    nested_counter -= 1

            if nested_counter == 0:
                if line_tokens.is_value_no_case(0, Keywords._ELSE):
                    ret.append(i)
                elif line_tokens.is_value_no_case(0, Keywords._ELIF):
                    ret.append(i)

        return ret

    @classmethod
    def parse(cls, parse_args):
        if_statements = cls.search_for_if_statements(parse_args.code_lines, parse_args.code_index)
        
    @classmethod
    def execute(cls, execute_args):
        pass

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
        pass

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
        pass

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
        pass

