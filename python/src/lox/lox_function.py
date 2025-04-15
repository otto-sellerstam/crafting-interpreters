from __future__ import annotations
from typing import Any, TYPE_CHECKING

from lox.lox_callable import LoxCallable
from lox.stmt import Function
from lox.namespace import Namespace
from lox.return_exception import Return
if TYPE_CHECKING: from lox.interpreter import Interpreter

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(
        self,
        interpreter: Interpreter,
        arguments: list[Any]
    ) -> Any:
        namespace = Namespace(interpreter.lox_globals)

        n_params = len(self.declaration.params)
        for i in range(n_params):
            namespace.define(
                self.declaration.params[i].lexeme,
                arguments[i],
            )

        try:
            interpreter.execute_block(
                self.declaration.body,
                namespace
            )
        except Return as ret:
            return ret.value

        return None
