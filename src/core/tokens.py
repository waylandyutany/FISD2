from io import BytesIO
from tokenize import tokenize
from tokenize import NUMBER as TOKEN_NUMBER
from tokenize import STRING as TOKEN_STRING
from tokenize import NAME as TOKEN_NAME
from tokenize import OP as TOKEN_OP

################################################################################
class Tokenizers:
    tokenizers = {}

    @classmethod
    def tokenize(cls, tokens):
        for tokenizer in cls.tokenizers:
            cls.tokenizers[tokenizer].tokenize(tokens)

################################################################################
def tokenizer_class(name):
    def _tokenizer_class(_class):
        Tokenizers.tokenizers[name] = _class
        return _class
    return _tokenizer_class

################################################################################
class Tokens:
    valid_tokens = [TOKEN_NAME, TOKEN_STRING, TOKEN_NUMBER, TOKEN_OP]

    def __init__(self, line, encoding = 'utf-8'):
        self._tokens = [[tok_id, tok_val] for tok_id, tok_val, _, _, _  in tokenize(BytesIO(line.encode(encoding)).readline) if tok_id in Tokens.valid_tokens]

    def insert_token(self, index, type, value):
        self._tokens.insert(index, [type, value])

    def empty(self):
        return len(self._tokens) == 0

    def token(self, index, tindex):
        try:
            return self._tokens[index][tindex]
        except:
            pass
        return None

    @property
    def tokens(self):
        return tuple(self._tokens)

    def is_name(self, index):
        return self.token(index, 0) == TOKEN_NAME

    def is_number(self, index):
        return self.token(index, 0) == TOKEN_NUMBER

    def is_string(self, index):
        return self.token(index, 0) == TOKEN_STRING

    def is_op(self, index):
        return self.token(index, 0) == TOKEN_OP

    def is_value(self, index, value):
        return self.token(index, 1) == value

