from core.tokens import Tokens, TOKEN_NUMBER, TOKEN_STRING, TOKEN_NONE, TOKEN_NATIVE
from copy import deepcopy

################################################################################
class Variable_stack:
    _VAR_TYPE = 'type'
    _VAR_VALUE = 'value'

    def __init__(self, _case_sensitive):
        self._case_sensitive = _case_sensitive
        self._stack = [{}]

################################################################################
    def to_json_dict(self):
        return {'_stack':deepcopy(self._stack)}

    def from_json_dict(self, json_dict):
        self._stack = json_dict['_stack']

################################################################################
    def find_variable(self, name):
        if not self._case_sensitive:
            name = name.lower()

        var_stack = self._stack[-1]
        if name in var_stack:
            return var_stack[name][Variable_stack._VAR_TYPE], var_stack[name][Variable_stack._VAR_VALUE]

        if len(self._stack) > 1:
            global_var_stack = self._stack[0]
            if name in global_var_stack:
                return global_var_stack[name][Variable_stack._VAR_TYPE], global_var_stack[name][Variable_stack._VAR_VALUE]

        return TOKEN_NONE, None

    def get_variable(self, name):
        type, value = self.find_variable(name)
        return value

    def set_variable(self, name, value):
        if not self._case_sensitive:
            name = name.lower()

        var_stack = self._stack[-1]

        if value == None:
            var_stack[name] = {Variable_stack._VAR_TYPE : TOKEN_NUMBER, Variable_stack._VAR_VALUE:None}
        elif isinstance(value, (list,set,tuple)):
            var_stack[name] = {Variable_stack._VAR_TYPE : TOKEN_NUMBER, Variable_stack._VAR_VALUE:value}
        elif isinstance(value, int):
            var_stack[name] = {Variable_stack._VAR_TYPE : TOKEN_NUMBER, Variable_stack._VAR_VALUE:value}
        elif isinstance(value, float):
            var_stack[name] = {Variable_stack._VAR_TYPE : TOKEN_NUMBER, Variable_stack._VAR_VALUE:value}
        else:
            var_stack[name] = {Variable_stack._VAR_TYPE : TOKEN_STRING, Variable_stack._VAR_VALUE:str(value)}

################################################################################
    def pop(self):
        self._stack.pop()

    def push(self):
        self._stack.append({})