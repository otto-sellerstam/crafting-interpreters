from __future__ import annotations
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass, field

from lox.exceptions.errors import LoxException
from lox.token.token import Token
from lox.abcs.lox_callable import LoxCallable
from lox.callables.lox_function import LoxFunction
if TYPE_CHECKING: from lox.interpreter import Interpreter

@dataclass
class LoxClass(LoxCallable):
    name: str
    methods: dict[str, LoxFunction]

    def call(
        self,
        interpreter: Interpreter,
        arguments: list[Any],
    ) -> Any:
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance
    
    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()
    
    def find_method(self, name: str) -> LoxFunction | None:
        if name in self.methods:
            return self.methods[name]
        
        return None

@dataclass
class LoxInstance:
    klass: LoxClass
    fields: dict[Token, Any] = field(default_factory=dict)

    def get(self, name: Token) -> Any:
        if name in self.fields:
            return self.fields[name]
        
        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)
        
        raise LoxException(f"Undefined attribute {name} on {self}")
    
    def set(self, name: Token, value: Any):
        self.fields[name] = value
