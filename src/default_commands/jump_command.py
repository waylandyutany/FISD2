from core.commands import command_class, Command
from core.code_line import Code_line
from core.tokens import Tokens

################################################################################
# Keywords
################################################################################
class Keywords:
    _JUMP = 'jump'

################################################################################
# JUMP Command
################################################################################
@command_class(Keywords._JUMP)
class JumpCommand(Command):
    @classmethod
    def parse(cls, pargs):
        pass    

    @classmethod
    def execute(cls, eargs):
        eargs.context.jump_to_code(Code_line.get_jump(eargs.code_line, Keywords._JUMP))

    @staticmethod
    def create_code_line(line_number, jump_label_name):
        tokens = Tokens(Keywords._JUMP)
        tokens.mark_as_keyword(0)
        code_line = Code_line.create(line_number, tokens, JumpCommand)
        Code_line.add_jump(code_line, Keywords._JUMP, jump_label_name)
        return code_line

