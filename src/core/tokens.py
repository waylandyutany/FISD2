from io import BytesIO
from copy import deepcopy
from tokenize import tokenize
from tokenize import NUMBER as TOKEN_NUMBER
from tokenize import STRING as TOKEN_STRING
from tokenize import NAME as TOKEN_NAME
from tokenize import OP as TOKEN_OP
TOKEN_KEYWORD = 0
TOKEN_NONE = -1
TOKEN_NATIVE = -2 # None, [],{},()

################################################################################
import math
_eval_funcs = {'cos':math.cos,
                'sin':math.sin,
                }

################################################################################
class Tokenizers:
    tokenizers = {}

    @classmethod
    def tokenize(cls, tokens, logger):
        for tokenizer in cls.tokenizers:
            cls.tokenizers[tokenizer].tokenize(tokens, logger)

################################################################################
def tokenizer_class(name=None):
    def _tokenizer_class(_class):
        Tokenizers.tokenizers[str(_class._keyword).lower()] = _class
        return _class
    return _tokenizer_class

################################################################################
class Tokens:
    valid_tokens = [TOKEN_NAME, TOKEN_STRING, TOKEN_NUMBER, TOKEN_OP]

################################################################################
    def __init__(self, line_or_tokens, encoding = 'utf-8'):
        if line_or_tokens == None:
            self._tokens = []
        elif isinstance(line_or_tokens, list):
            self._tokens = line_or_tokens
        else:
            self._tokens = [ [tok_id, tok_val]\
               for tok_id, tok_val, _, _, _  in tokenize(BytesIO(line_or_tokens.encode(encoding)).readline) if tok_id in Tokens.valid_tokens\
              ]

    def init_from_string(self, string, encoding = 'utf-8'):
        self._tokens = [ [tok_id, tok_val]\
            for tok_id, tok_val, _, _, _  in tokenize(BytesIO(string.encode(encoding)).readline) if tok_id in Tokens.valid_tokens\
            ]

    def __str__(self):
        return ", ".join([tok[1] for tok in self._tokens])

    def to_string(self,fmt = " "):
        return fmt.join([tok[1] for tok in self._tokens])

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

    def find_op(self, op):#@todo why not use find_ops instead?!?!
        for i in range(0, len(self._tokens)):
            if self.is_op(i) and self.is_value(i,op):
                return i
        return None

    def find_ops(self, op):
        return [i for i in range(0, len(self)) if self.is_op(i) and self.is_value(i,op)]

    def split_tokens_by_op(self, op = ','):
        ret = []
        ops = [-1, len(self)]
        ops[1:1] = self.find_ops(op)
        return [ self.sub_tokens(ops[i],ops[i+1]) for i in range(0, len(ops)-1)]

    def sub_tokens(self, start, end):
        ''' create new Tokens from tokens between (start, end) '''
        return Tokens(deepcopy(self._tokens[start + 1 : end]))

    def pop_tokens(self, start, end):
        ''' remove tokens between (start, end) and returns them '''
        ret = Tokens("")
        ret._tokens = self._tokens[start + 1 : end]
        del self._tokens[start + 1 : end]
        return ret

    def insert_name(self, index, value):
        self._tokens.insert(index, [TOKEN_NAME, value])

    def insert_op(self, index, value):
        self._tokens.insert(index, [TOKEN_OP, value])

################################################################################
    def is_name(self, index):
        return self.__token(index, 0) == TOKEN_NAME

    def is_number(self, index):
        return self.__token(index, 0) == TOKEN_NUMBER

    def is_string(self, index):
        return self.__token(index, 0) == TOKEN_STRING

    def is_op(self, index):
        return self.__token(index, 0) == TOKEN_OP

    def is_op_value(self, index, value):
        return self.is_op(index) and self.is_value(index, value)

    def is_keyword(self, index):
        return self.__token(index, 0) == TOKEN_KEYWORD

    def is_native(self, index):
        return self.__token(index, 0) == TOKEN_NATIVE

    def is_value(self, index, value):
        if self.is_string(index):
            return self.value_str(index) == str(value)
        return self.value(index) == value

    def is_value_no_case(self, index, value):
        if isinstance(value,(list, tuple)):
            return any((self.value_str(index).lower() == str(v).lower() for v in value))
        return self.value_str(index).lower() == str(value).lower()
################################################################################
    def value(self, index):
        ''' return string as "string" '''
        if self.is_number(index):
            try:
                return int(self.__token(index, 1))
            except:
                return  float(self.__token(index, 1))
        return self.__token(index, 1)

    def value_str(self, index):
        ''' return string as string '''
        if self.is_string(index):
            return self.__token(index, 1)[1:-1]
        return str(self.__token(index, 1))

################################################################################
    def set_string(self, index, string):
        try:
            self._tokens[index][0] = TOKEN_STRING
            self._tokens[index][1] = '"{}"'.format(string)
        except:pass

    def set_number(self, index, number):
        try:
            self._tokens[index][0] = TOKEN_NUMBER
            self._tokens[index][1] = number
        except:pass

    def set_native(self, index, native):
        try:
            self._tokens[index][0] = TOKEN_NATIVE
            self._tokens[index][1] = native
        except:pass

    def mark_as_keyword(self, index):
        try:
            self._tokens[index][0] = TOKEN_KEYWORD
        except:pass

################################################################################
    def search_keywords_in_tokens(self, keywords):
        return [i for i in range(0, len(self)) if self.is_keyword(i) and self.is_value_no_case(i, keywords)]

    def mark_tokens_as_keywords(self, keywords):
        for i in range(0, len(self)):
            if self.is_name(i):
                if self.is_value_no_case(i, keywords):
                    self.mark_as_keyword(i)

################################################################################
    def evaluation_string(self, start_index, end_index):
        return " ".join((str(self.value(i)) for i in range(start_index + 1, end_index)))

    #@todo handle better error with more details in exception, test it ! :-)
    def evaluate_tokens(self, start_index, end_index):
        try:
            str_to_evaluate = self.evaluation_string(start_index, end_index)
            e = eval(self.evaluation_string(start_index, end_index), {'__builtins__':None}, _eval_funcs)
            return e
        except BaseException as e:
            raise Exception("'{}' in '{}'".format(e, str_to_evaluate))

    def evaluate(self):
        return self.evaluate_tokens(-1, len(self))

    def string_to_evaluate(self):
        return self.evaluation_string(-1, len(self))


