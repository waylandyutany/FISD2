from core.tokens import Tokens
from copy import deepcopy

################################################################################
class RawArguments(Tokens):
    def __init__(self, tokens):
        self._tokens = deepcopy(tokens.tokens()[:])
