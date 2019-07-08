from copy import deepcopy
################################################################################

class SystemVariables:
    def __init__(self):
        self.__variables = {}

    def to_json_dict(self):
        return {'variables':deepcopy(self.__variables)}

    def from_json_dict(self, json_dict):
        self.__variables = json_dict['variables']
