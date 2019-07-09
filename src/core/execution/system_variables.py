from copy import deepcopy
################################################################################

class SystemVariables:
    def __init__(self, _case_sensitive):
        self._case_sensitive = _case_sensitive
        self.__variables = {}

    def to_json_dict(self):
        return {'variables':deepcopy(self.__variables)}

    def from_json_dict(self, json_dict):
        self.__variables = json_dict['variables']

    def set(self, name, value):
        if not self._case_sensitive:
            name = name.lower()

        self.__variables[name] = value

    def get(self, name, default_value = None):
        if not self._case_sensitive:
            name = name.lower()

        if name in self.__variables:
            return self.__variables[name]
        return default_value
