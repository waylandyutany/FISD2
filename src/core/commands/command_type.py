################################################################################
class BaseCommand:
    def __init__(self):
        pass

    def preprocess_line_tokens(self, line_tokens):
        pass

################################################################################
class CallableCommand(BaseCommand):
    # if pass_evaluated_args True, evaluated arguments are passed within execute(cls, params, ...)
    # and returned value is automaticaly set to context
    def __init__(self, pass_evaluated_args = False):
        self.__pass_evaluated_args = pass_evaluated_args
        super().__init__()

    def preprocess_line_tokens(self, line_tokens):
        if not line_tokens.is_op_value(1,'('):
            line_tokens.insert_op(1,'(')
            line_tokens.insert_op(len(line_tokens),')')
            pass

    @property
    def pass_evaluated_args(self):
        return self.__pass_evaluated_args