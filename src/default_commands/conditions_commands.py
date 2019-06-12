from core.commands import command_class, Command
from default_commands.default_commands import JumpCommand
from core.code_line import Code_line

################################################################################
# IF Command
################################################################################
@command_class()
class IfCommand(Command):
    _IF = 'if'
    _END_IF = 'endif'
    _THEN = 'then'
    _ELSE = 'else'
    _ELIF = 'elif'

    _keyword = _IF
    _keywords = [_THEN]

    @classmethod
    def search_for_if_commands(cls, code_lines, code_index):
        ''' Returns code indicies for all if conditional commands (if, elif, else, endif)'''
        ret = []
        nested_counter = 0
        ret.append(code_index)
        for i in range(code_index + 1, len(code_lines)):
            _, line_tokens, _ = Code_line.split(code_lines[i])

            if line_tokens.is_value_no_case(0, cls._IF):
                nested_counter += 1

            if line_tokens.is_value_no_case(0, cls._END_IF):
               if nested_counter == 0:
                    ret.append(i)
                    return ret
               else:
                    nested_counter -= 1

            if nested_counter == 0:
                if line_tokens.is_value_no_case(0, [cls._ELSE, cls._ELIF]):
                    ret.append(i)

        return None #When no endif found!

    @classmethod
    def parse(cls, pargs):
        #@todo error when no correct order if, elif..., else, endif
        #@todo error when no endif
        if_commands = cls.search_for_if_commands(pargs.code_lines, pargs.code_index)

        end_if_label_name = pargs.code_labels.get_label_name(IfCommand._END_IF)
        Code_line.add_label(pargs.code_lines[if_commands[-1]], end_if_label_name)

        #add jumps to next elif, else commands marked with their labels
        for i in range(0, len(if_commands) - 1):
            next_if_label_name = pargs.code_labels.get_label_name(IfCommand._ELSE)
            Code_line.add_label(pargs.code_lines[if_commands[i + 1]], next_if_label_name)
            Code_line.add_jump(pargs.code_lines[if_commands[i]], IfCommand._ELSE, next_if_label_name)

        # inserting jump command before each elif or else
        for i in range(1, len(if_commands) - 1):
            line_number = Code_line.get_line_number(pargs.code_lines[if_commands[i]])
            jump_code_line = JumpCommand.create_code_line(line_number, end_if_label_name)
            pargs.code_lines_insertion.insert_before(line_number, jump_code_line)

    @staticmethod
    def execute(eargs):
        if not eargs.arguments.evaluate_tokens(0, len(eargs.arguments) - 1):
            eargs.context.jump_to_code(Code_line.get_jump(eargs.code_line, IfCommand._ELSE))

################################################################################
# ENDIF Command
################################################################################
@command_class()
class EndIfProcCommand(Command):
    _keyword = IfCommand._END_IF

    @staticmethod
    def parse(pargs):
        pass

    @staticmethod
    def execute(eargs):
        pass

################################################################################
# ELSE Command
################################################################################
@command_class()
class ElseProcCommand(Command):
    _keyword = IfCommand._ELSE

    @staticmethod
    def parse(pargs):
        pass

    @staticmethod
    def execute(eargs):
        pass

################################################################################
# ELIF Command
################################################################################
@command_class()
class ElifProcCommand(Command):
    _keyword = IfCommand._ELIF
    _keywords = [IfCommand._THEN]

    @staticmethod
    def parse(pargs):
        pass

    @staticmethod
    def execute(eargs):
        IfCommand.execute(eargs)
