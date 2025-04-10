from typing import Any

from lox.token import Token

class LoxNameError(NameError):
    pass

class Environment:
    values: dict[str, Any] = {}

    def define(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        else:
            raise LoxNameError

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise LoxNameError
