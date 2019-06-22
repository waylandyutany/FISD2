################################################################################
class Execution_args: 
    #@ properties for tokens, ..., code_line is property as well, for Parse arguments as well !!! optimize second call of property !!!
    def __init__(self, _context, _logger, _code_name, _code_lines):
        self.code_name = _code_name
        self.code_lines = _code_lines
        self.code_index = None
        self.code_line = None

        self.arguments = None

        self.context = _context
        self.logger = _logger
