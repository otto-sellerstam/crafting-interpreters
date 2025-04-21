from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from lox.token.token import Token

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
        def visit_call_expr(self, expr: Call) -> T:
            """Process a call expression.
            
            Args:
                expr: The call expression to process.
            """
            pass

        @abstractmethod
        def visit_get_expr(self, expr: Get) -> T:
            """Process a get expression.
            
            Args:
                expr: The get expression to process.
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
        def visit_logical_expr(self, expr: Logical) -> T:
            """Process a unary expression.
            
            Args:
                expr: The unary expression to process.
            """
            pass

        @abstractmethod
        def visit_set_expr(self, expr: Set) -> T:
            """Process a set expression.
            
            Args:
                expr: The set expression to process.
            """
            pass

        @abstractmethod
        def visit_this_expr(self, expr: This) -> T:
            """Process a this expression.
            
            Args:
                expr: The this expression to process.
            """
            pass

        @abstractmethod
        def visit_unary_expr(self, expr: Unary) -> T:
            """Process a unary expression.
            
            Args:
                expr: The unary expression to process.
            """
            pass

        @abstractmethod
        def visit_variable_expr(self, expr: Variable) -> T:
            """Process a variable expression.
            
            Args:
                expr: The variable expression to process.
            """
            pass

        @abstractmethod
        def visit_assign_expr(self, expr: Assign) -> T:
            """Process a assign expression.
            
            Args:
                expr: The assign expression to process.
            """
            pass

#
# Side note: NamedTuples would probably be preferrable here, but would result
# in a clash of metaclasses.
#
# One would be to to combine NamedTypleMeta and ABCMeta.
#
@dataclass(frozen=True)
class Binary(Expr):
    """Represents a binary operation expression."""
    left: Expr
    operator: Token
    right: Expr

    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_binary_expr(self)

@dataclass(frozen=True)
class Call(Expr):
    callee: Expr
    arguments: list[Expr]
    paren: Token  # To report potential runtime errors.
    
    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_call_expr(self)

@dataclass(frozen=True)
class Get(Expr):
    obj: Expr
    name: Token

    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_get_expr(self)

@dataclass(frozen=True)
class Grouping(Expr):
    """Represents a parenthesized expression."""
    expression: Expr
    
    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_grouping_expr(self)

@dataclass(frozen=True)
class Literal(Expr):
    """Represents a literal value expression."""
    value: Any
    
    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_literal_expr(self)

@dataclass(frozen=True)
class Logical(Expr):
    """Represents a literal value expression."""
    left: Expr
    operator: Token
    right: Expr

    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_logical_expr(self)

@dataclass(frozen=True)
class Set(Expr):
    obj: Expr
    name: Token
    value: Expr

    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_set_expr(self)

@dataclass(frozen=True)
class This(Expr):
    keyword: Token
    
    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_this_expr(self)

@dataclass(frozen=True)
class Unary(Expr):
    """Represents a unary operation expression."""
    operator: Token
    right: Expr
    
    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_unary_expr(self)

@dataclass(frozen=True)
class Variable(Expr):
    """Represents a unary operation expression."""
    name: Token
    
    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_variable_expr(self)

@dataclass(frozen=True)
class Assign(Expr):
    """Represents a unary operation expression."""
    name: Token
    value: Expr
    
    def accept[T](self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_assign_expr(self)
