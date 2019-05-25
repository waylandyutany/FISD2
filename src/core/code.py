from io import BytesIO
from tokenize import tokenize, NUMBER, STRING, NAME, OP, COMMENT

types = { NUMBER : "NUMBER",
         STRING : "STRING",
         NAME : "NAME",
         OP : "OP",
         COMMENT : "COMMENT"
         }

class Code:
    def __init__(self):
        pass

    def load_from_file(self, file_name):
        with open(file_name) as f:
            for line in f.readlines():
                result = []
                tokens = tokenize(BytesIO(line.encode('utf-8')).readline)
                for toknum, tokval, _, _, _  in tokens:
                    if toknum in types:
                        print(types[toknum], tokval)
                    else:
                        print("Unknown {} {}".format(toknum, tokval))
