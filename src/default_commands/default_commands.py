from core.commands import command_class, Command
from core.tokens import tokenizer_class, TOKEN_NAME
from core.code_line import Code_line

from default_commands.evaluation_commands import Code_evaluation

################################################################################
# JUMP Command
################################################################################
@command_class()
class JumpCommand(Command):
    _JUMP = 'jump'
    _keyword = _JUMP

    @staticmethod
    def parse(pargs):
        pass    

    @staticmethod
    def execute(eargs):
        eargs.context.jump_to_code(Code_line.get_jump(eargs.code_line, JumpCommand._keyword))

    @staticmethod
    def create_code_line(line_number, jump_label_name):
        tokens = Tokens(JumpCommand._keyword)
        tokens.mark_as_keyword(0)
        code_line = Code_line.create(line_number, tokens, JumpCommand)
        Code_line.add_jump(code_line, JumpCommand._keyword, jump_label_name)
        return code_line
        
################################################################################
# SET Command
################################################################################
@command_class()
@tokenizer_class()
class SetCommand(Command):
    _keyword = 'set'

    @classmethod
    def parse(cls, pargs):
        Code_evaluation.evaluate_function_calls(pargs)
        line_tokens = Code_line.get_line_tokens(pargs.code_line)
        line_tokens.mark_as_keyword(1)

    @staticmethod
    def execute(eargs):
        variable_name = eargs.arguments.value(1)
        try:
            evaluated_value = eargs.arguments.evaluate_tokens(2, len(eargs.arguments))
        except Exception as e:
            eargs.logger.error("Exception during '{}' evaluation! {}!".format(variable_name, e))
            return

        #context.logger.debug("'{}' evaluated '{} = {}'".format(variable_name, string_to_evaluate, evaluated_value))

        eargs.context.set_variable(variable_name, evaluated_value)

    @staticmethod
    def tokenize(tokens, logger):
        if tokens.is_name(0) and tokens.is_op(1) and tokens.is_value(1, '='):
            tokens.insert_name(0, SetCommand._keyword)

################################################################################
# PRINT Command
################################################################################
@command_class()
class PrintCommand(Command):
    _keyword = 'print'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.logger.info("PRINT {}".format("".join( ( str(eargs.arguments.value_str(i)) for i in range(1, len(eargs.arguments)) ) )))

################################################################################
# EXECUTE Command
################################################################################
@command_class()
class ExecuteCommand(Command):
    _keyword = 'execute'

    @classmethod
    def parse(cls, pargs):
        pass

    @classmethod
    def execute(cls, eargs):
        eargs.context.execute_code(eargs.arguments.value_str(1))

