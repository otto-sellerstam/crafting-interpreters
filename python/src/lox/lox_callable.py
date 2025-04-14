from abc import ABC, abstractmethod

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING: from lox.interpreter import Interpreter

class LoxCallable(ABC):
    
    @abstractmethod
    def call(
        self,
        interpreter: 'Interpreter',
        arguments: list[Any]
    ) -> Any:
        pass

    @abstractmethod
    def arity(self) -> int:
        return 0
