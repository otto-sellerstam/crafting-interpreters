class LoxException(Exception):
    pass

class LoxSyntaxError(SyntaxError, LoxException):
    pass

class LoxNameError(NameError, LoxException):
    pass
