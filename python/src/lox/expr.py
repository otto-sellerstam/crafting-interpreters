from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from lox.token import Token

class Expr(ABC):
    """Base class for all expression types in the Lox language."""
    @abstractmethod
    def accept[T](self, visitor: Visitor[T]) -> T:
        """Accept a visitor to process this expression.
        
        Args:
            visitor: The visitor to process this expression.
        
        Returns:
            The result of the visitor's processing.
        """
        pass

class Visitor[T](ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: Binary) -> T:
        """Process a binary expression.
        
        Args:
            expr: The binary expression to process.
        """
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping) -> T:
        """Process a grouping expression.
        
        Args:
            expr: The grouping expression to process.
        """
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: Literal) -> T:
        """Process a literal expression.
        
        Args:
            expr: The literal expression to process.
        """
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: Unary) -> T:
        """Process a unary expression.
        
        Args:
            expr: The unary expression to process.
        """
        pass

##
# Side note: NamedTuples would probably be preferrable here, but would result
# in a clash of metaclasses.
##

@dataclass(frozen=True)
class Binary(Expr):
    """Represents a binary operation expression."""
    left: Expr
    operator: Token
    right: Expr

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_binary_expr(self)

@dataclass(frozen=True)
class Grouping(Expr):
    """Represents a parenthesized expression."""
    expression: Expr
    
    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_grouping_expr(self)

@dataclass(frozen=True)
class Literal(Expr):
    """Represents a literal value expression."""
    value: Any
    
    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_literal_expr(self)

@dataclass(frozen=True)
class Unary(Expr):
    """Represents a unary operation expression."""
    operator: Token
    right: Expr
    
    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_unary_expr(self)
