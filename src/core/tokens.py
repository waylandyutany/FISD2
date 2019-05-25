class Tokenizers:
    tokenizers = {}

    @classmethod
    def tokenize(cls, tokens):
        for tokenizer in Tokenizers.tokenizers:
            tokens = Tokenizers.tokenizers[tokenizer].tokenize(tokens)
        return tokens

def tokenizer_class(name):
    def _tokenizer_class(_class):
        Tokenizers.tokenizers[name] = _class
        return _class
    return _tokenizer_class

class Tokens:
    def __init__(self, line):
        pass
