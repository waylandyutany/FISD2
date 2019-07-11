################################################################################
class BaseCommand:
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)    

    def preprocess_line_tokens(self, line_tokens):
        pass

################################################################################
class CallableCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def preprocess_line_tokens(self, line_tokens):
        if not line_tokens.is_op_value(1,'('):
            line_tokens.insert_op(1,'(')
            line_tokens.insert_op(len(line_tokens),')')
            pass
