class LoxException(Exception):
    pass

class LoxSyntaxError(LoxException):
    pass

class LoxNameError(LoxException):
    pass

class LoxArgumentError(LoxException):
    pass

class LoxTypeError(LoxException):
    pass
