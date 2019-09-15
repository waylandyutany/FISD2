################################################################################
class Call_signature:
    @classmethod
    def create_from_signature(cls, signature):
        return Call_signature({})

    @classmethod
    def create_from_function_code_lines(cls, code_lines):
        return Call_signature({})

    def resolve(self, logger, line_tokens):
        pass

################################################################################
    def __init__(self, json_dict):
        pass

    def to_json_dict(self):
        return None