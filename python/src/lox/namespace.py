from __future__ import annotations
from typing import Any

from lox.token.token import Token
from lox.exceptions.errors import LoxNameError

class Namespace:
    def __init__(self, enclosing: Namespace | None = None):
        self.enclosing = enclosing  # None is global scope.
        self.values: dict[str, Any] = {}

    def define(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxNameError(f"Variable '{name.lexeme}' not defined")

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            if self.values[name.lexeme] is None:
                raise LoxNameError(f"Variable '{name.lexeme}' not initialized")
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxNameError(f"Variable '{name.lexeme}' not defined")
