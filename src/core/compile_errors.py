################################################################################
class Error:
    def __init__(self, _code, _string):
        self.code = _code
        self.string = _string

    def __str__(self):
        return "({}){}".format(self.code, self.string)

################################################################################
def non_existing_file_name(file_name):
    return Error(0, "Non existing file name '{}'!".format(file_name))

################################################################################
