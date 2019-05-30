from io import BytesIO
from tokenize import tokenize
from tokenize import NUMBER as TOKEN_NUMBER
from tokenize import STRING as TOKEN_STRING
from tokenize import NAME as TOKEN_NAME
from tokenize import OP as TOKEN_OP
TOKEN_KEYWORD = 0

################################################################################
class Tokenizers:
    tokenizers = {}

    @classmethod
    def tokenize(cls, tokens, logger):
        for tokenizer in cls.tokenizers:
            cls.tokenizers[tokenizer].tokenize(tokens, logger)

################################################################################
def tokenizer_class(name):
    def _tokenizer_class(_class):
        Tokenizers.tokenizers[str(name).lower()] = _class
        return _class
    return _tokenizer_class

################################################################################
class Tokens:
    valid_tokens = [TOKEN_NAME, TOKEN_STRING, TOKEN_NUMBER, TOKEN_OP]

################################################################################
    def __init__(self, line, encoding = 'utf-8'):
        self._tokens = [[tok_id, tok_val] for tok_id, tok_val, _, _, _  in tokenize(BytesIO(line.encode(encoding)).readline) if tok_id in Tokens.valid_tokens]

    def __str__(self):
        return ", ".join([tok[1] for tok in self._tokens])

    def __len__(self):
        return len(self._tokens)

    def __token(self, index, tindex):
        try:
            return self._tokens[index][tindex]
        except:
            pass
        return None

################################################################################
    def empty(self):
        return len(self._tokens) == 0

    def tokens(self):
        return self._tokens

################################################################################
    def is_name(self, index):
        return self.__token(index, 0) == TOKEN_NAME

    def is_number(self, index):
        return self.__token(index, 0) == TOKEN_NUMBER

    def is_string(self, index):
        return self.__token(index, 0) == TOKEN_STRING

    def is_op(self, index):
        return self.__token(index, 0) == TOKEN_OP

    def is_keyword(self, index):
        return self.__token(index, 0) == TOKEN_KEYWORD

    def is_value(self, index, value):
        return self.__token(index, 1) == value

    def is_value_no_case(self, index, value):
        return str(self.__token(index, 1)).lower() == str(value).lower()

    def value(self, index):
        return self.__token(index, 1)

    def value_str(self, index):
        if self.is_string(index):
            return self.__token(index, 1)[1:-1]
        return str(self.__token(index, 1))

################################################################################
    def set_string(self, index, string):
        self._tokens[index][0] = TOKEN_STRING
        self._tokens[index][1] = '"{}"'.format(string)

    def set_keyword(self, index):
        self._tokens[index][0] = TOKEN_KEYWORD

################################################################################
    def insert_name(self, index, value):
        self._tokens.insert(index, [TOKEN_NAME, value])

################################################################################
