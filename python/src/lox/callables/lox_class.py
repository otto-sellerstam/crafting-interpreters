from __future__ import annotations
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass, field

from lox.exceptions.errors import LoxException
from lox.token.token import Token
from lox.abcs.lox_callable import LoxCallable
if TYPE_CHECKING: from lox.interpreter import Interpreter

@dataclass
class LoxClass(LoxCallable):
    name: str

    def call(
        self,
        interpreter: Interpreter,
        arguments: list[Any]
    ) -> Any:
        instance = LoxInstance(self)
        return instance
    
    def arity(self) -> int:
        return 0

@dataclass
class LoxInstance:
    klass: LoxClass
    fields: dict[Token, Any] = field(default_factory=dict)

    def get(self, name: Token) -> Any:
        if name in self.fields:
            return self.fields[name]
        
        raise LoxException("Undefined attribute")
    
    def set(self, name: Token, value: Any):
        self.fields[name] = value
