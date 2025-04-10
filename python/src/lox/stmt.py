from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from lox.token import Token
from lox.expr import Expr

class Stmt(ABC):
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
        def visit_expression_stmt(self, stmt: Expression) -> T:
            """Process an expression statement.
            
            Args:
                expr: The expression statement to process.
            """
            pass

        @abstractmethod
        def visit_print_stmt(self, stmt: Print) -> T:
            """Process a print statement.
            
            Args:
                expr: The print statement to process.
            """
            pass

        @abstractmethod
        def visit_var_stmt(self, stmt: Var) -> T:
            """Process a print statement.
            
            Args:
                expr: The print statement to process.
            """
            pass

#
# Side note: NamedTuples would probably be preferrable here, but would result
# in a clash of metaclasses.
#
# One would be to to combine NamedTypleMeta and ABCMeta.
#
@dataclass(frozen=True)
class Expression(Stmt):
    expression: Expr

    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_expression_stmt(self)

@dataclass(frozen=True)
class Print(Stmt):
    expression: Expr

    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_print_stmt(self)

@dataclass(frozen=True)
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_var_stmt(self)

