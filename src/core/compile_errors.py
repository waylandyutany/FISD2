################################################################################
class Error:
    def __init__(self, _code, _string):
        self.code = _code
        self.string = _string

    def __str__(self):
        return "({}){}".format(self.code, self.string)

################################################################################
class CompileError(Error):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    ################################################################################
    @staticmethod
    def non_existing_file_name(file_name):
        return CompileError(0, "Non existing file name '{}'!".format(file_name))

    @staticmethod
    def unknown_command(command_name):
        return CompileError(1, "Unknown command '{}'!".format(command_name))

    @staticmethod
    def invalid_command(command_name):
        return CompileError(2, "Invalid command '{}'!".format(command_name))

################################################################################
