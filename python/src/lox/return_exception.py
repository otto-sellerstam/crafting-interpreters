'''
This class is used for control flow, which is generally not optimal, but I
think it can be justified here. I'll ask on SO or Reddit later!
'''

from typing import Any

class Return(Exception):
    def __init__(
        self,
        value: Any,
        message: str | None= None,
    ):
        self.value = value
        super().__init__(message or str(value))
