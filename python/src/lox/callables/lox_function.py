from __future__ import annotations
from typing import Any, Final, TYPE_CHECKING
from dataclasses import dataclass

from lox.abcs.lox_callable import LoxCallable
from lox.abcs.stmt import Function
from lox.namespace import Namespace
from lox.control_flow_exceptions.return_exception import Return
if TYPE_CHECKING: from lox.interpreter import Interpreter

@dataclass
class LoxFunction(LoxCallable):
    declaration: Final[Function]
    closure: Final[Namespace]

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(
        self,
        interpreter: Interpreter,
        arguments: list[Any]
    ) -> Any:
        # We put the closure as the enclosing namespace.
        namespace = Namespace(self.closure)

        n_params = len(self.declaration.params)
        for i in range(n_params):
            namespace[
                self.declaration.params[i].lexeme
            ] = arguments[i]

        try:
            interpreter.execute_block(
                self.declaration.body,
                namespace
            )
        except Return as ret:
            return ret.value

        return None
