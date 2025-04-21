from enum import Enum, auto

class FunctionType(Enum):
    NONE = None
    FUNCTION = auto()
    METHOD = auto()
    INITIALIZER = auto()