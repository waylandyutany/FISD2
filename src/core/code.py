from io import BytesIO
from tokenize import tokenize, NUMBER, STRING, NAME, OP, COMMENT

valid_token_ids = [NAME, STRING, NUMBER, OP]
encoding = 'utf-8'

tokenizer_funcs = {}

def tokenizer(name):
    def _tokenizer(tokenizer_func):
        tokenizer_funcs[name] = tokenizer_func
    return _tokenizer

class Code:
    def __init__(self):
        pass

    def compile_from_file(self, file_name):
        with open(file_name) as f:
            line_number = 0
            for line in f.readlines():
                line_number = line_number + 1

                line_tokens = [{'id':tok_id, 'val':tok_val} for tok_id, tok_val, _, _, _  in tokenize(BytesIO(line.encode(encoding)).readline) if tok_id in valid_token_ids]
                for tokenizer in tokenizer_funcs:
                    line_tokens = tokenizer_funcs[tokenizer](line_tokens)

                if len(line_tokens) > 0:
                    print("line {} : {}".format(line_number, line_tokens))
