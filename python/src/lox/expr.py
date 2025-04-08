from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from python.src.lox.token import Token

class Expr(ABC):
    @abstractmethod
    def accept():
        pass

class Visitor[T](ABC):
    @abstractmethod
    def visit_binary_expr(expr: Binary) -> T:
        pass

    @abstractmethod
    def visit_grouping_expr(expr: Grouping) -> T:
        pass

    @abstractmethod
    def visit_literal_expr(expr: Literal) -> T:
        pass

    @abstractmethod
    def visit_unary_expr(expr: Unary) -> T:
        pass

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_binary_expr(self)

@dataclass
class Grouping(Expr):
    expression: Expr
    
    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_grouping_expr(self)

@dataclass
class Literal(Expr):
    literal: Any
    
    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_literal_expr(self)

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr
    
    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_unary_expr(self)
