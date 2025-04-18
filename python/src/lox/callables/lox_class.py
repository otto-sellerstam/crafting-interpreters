from __future__ import annotations
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass

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
