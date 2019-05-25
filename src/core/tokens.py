from io import BytesIO
from tokenize import tokenize
from tokenize import NUMBER as TOKEN_NUMBER
from tokenize import STRING as TOKEN_STRING
from tokenize import NAME as TOKEN_NAME
from tokenize import OP as TOKEN_OP

TOKEN_NONE = None

class Tokenizers:
    tokenizers = {}

    @classmethod
    def tokenize(cls, tokens):
        for tokenizer in Tokenizers.tokenizers:
            Tokenizers.tokenizers[tokenizer].tokenize(tokens)

def tokenizer_class(name):
    def _tokenizer_class(_class):
        Tokenizers.tokenizers[name] = _class
        return _class
    return _tokenizer_class

class Tokens:
    valid_tokens = [TOKEN_NAME, TOKEN_STRING, TOKEN_NUMBER, TOKEN_OP]

    def __init__(self, line, encoding = 'utf-8'):
        self.tokens = [{'id':tok_id, 'val':tok_val} for tok_id, tok_val, _, _, _  in tokenize(BytesIO(line.encode(encoding)).readline) if tok_id in Tokens.valid_tokens]

    def insert_token(self, index, type, value):
        self.tokens.insert(index, {'id':type, 'val':value})