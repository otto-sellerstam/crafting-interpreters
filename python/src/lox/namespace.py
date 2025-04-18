from __future__ import annotations
from typing import Any
from collections.abc import MutableMapping, Iterable

from lox.exceptions.errors import LoxNameError

class Namespace(MutableMapping[str, Any]):
    def __init__(self, enclosing: Namespace | None = None):
        self.enclosing = enclosing  # None is global scope.
        self.values: dict[str, Any] = {}

    def __getitem__(self, name: str) -> Any:
        if name in self.values:
            if self.values[name] is None:
                raise LoxNameError(f"Variable '{name}' not initialized")
            return self.values[name]

        if self.enclosing is not None:
            return self.enclosing[name]

        raise LoxNameError(f"Variable '{name}' not defined")

    def __setitem__(self, name: str, value: Any):
        self.values[name] = value

    def __delitem__(self, name: str) -> None:
        del self.values[name]

    def __iter__(self) -> Iterable[str]:
        return iter(self.values)
    
    def __len__(self) -> int:
        return len(self.values)

    def ancestor(self, distance: int) -> Namespace:
        '''
        Gets the ancerstor at distance from self.
        '''
        ancestor = self
        for _ in range(distance):
            if ancestor.enclosing is not None:
                ancestor = ancestor.enclosing
        return ancestor

    def assign(self, name: str, value: Any):
        '''
        Assigns to a variable in the nearest namespace
        where the variable is defined (done via __getitem__).
        '''
        if name in self.values:
            self[name] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxNameError(f"Variable '{name}' not defined")

