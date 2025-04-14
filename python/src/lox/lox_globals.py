from typing import TYPE_CHECKING, Any
import time

from lox.lox_callable import LoxCallable
if TYPE_CHECKING: from lox.interpreter import Interpreter

### To be honest, this structure is probably not very pythonic.
class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(
        self,
        interpreter: 'Interpreter',
        arguments: list[Any]
    ) -> Any:
        return time.time()

    def __str__(self):
        return '<native fn>'