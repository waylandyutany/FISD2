from core.code import Code

################################################################################
class Arguments:
    def __init__(self, tokens):
        self._tokens = tokens

################################################################################
class Context:
    _CODE_FILE = 'code_file'
    _CODE_INDEX = 'code_index'

    def __init__(self, code):
        self._code = code
        self._call_stack = []

################################################################################
    def execute_code(self, code_file_name, logger, call_stack_index = None):
        #getting code lines from the code
        code_lines = self._code.get_file_code(code_file_name)

        #creating code context
        call_context = {Context._CODE_FILE:code_file_name, Context._CODE_INDEX:0}

        #pushing code context to the stack
        self._call_stack.append(call_context)

        #executing commands
        for code_index in range(call_context[Context._CODE_INDEX], len(code_lines)):
            call_context[Context._CODE_INDEX] = code_index

            line_number, line_tokens, command_class = Code.split_code_line(code_lines[code_index])

            logger.preface = "'{}'[{}] : ".format(code_file_name, line_number)

            command_class.execute(self, line_tokens, logger)
            
        #popping code context from code stack
        self._call_stack.pop()

################################################################################
    def run(self, logger):
        self.execute_code(self._code.main_file_name(), logger)

    def run_from_call_stack(self, call_stack, logger):
        pass
################################################################################
