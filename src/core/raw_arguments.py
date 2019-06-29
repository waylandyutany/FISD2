from core.tokens import Tokens, TOKEN_NUMBER, TOKEN_STRING, TOKEN_NONE, TOKEN_NATIVE
from copy import deepcopy

################################################################################
class RawArguments(Tokens):
    def __init__(self, variables, tokens):
        self._tokens = deepcopy(tokens.tokens()[:])
        for i in range(0, len(self)):
            if self.is_name(i):
                type, value = variables.find_variable(self.value(i))
                if type == TOKEN_NUMBER:
                    self.set_number(i, value)
                elif type == TOKEN_STRING:
                    self.set_string(i, value)
                elif type == TOKEN_NATIVE:
                    self.set_native(i, value)
