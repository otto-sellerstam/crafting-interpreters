from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from lox.token.token import Token
from lox.abcs.expr import Expr

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
        def visit_function_stmt(self, stmt: Function) -> T:
            """Process a function statement.
            
            Args:
                expr: The function statement to process.
            """
            pass

        @abstractmethod
        def visit_return_stmt(self, stmt: Return) -> T:
            """Process a return statement.
            
            Args:
                expr: The return statement to process.
            """
            pass

        @abstractmethod
        def visit_if_stmt(self, stmt: If) -> T:
            """Process an if statement.
            
            Args:
                expr: The if statement to process.
            """
            pass

        @abstractmethod
        def visit_while_stmt(self, stmt: While) -> T:
            """Process a while statement.
            
            Args:
                expr: The while statement to process.
            """
            pass

        @abstractmethod
        def visit_break_stmt(self, stmt: Break) -> T:
            """Process a break statement.
            
            Args:
                expr: The break statement to process.
            """
            pass

        @abstractmethod
        def visit_var_stmt(self, stmt: Var) -> T:
            """Process a var statement.
            
            Args:
                expr: The var statement to process.
            """
            pass

        @abstractmethod
        def visit_block_stmt(self, stmt: Block) -> T:
            """Process a block statement.
            
            Args:
                expr: The block statement to process.
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
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]

    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_function_stmt(self)

@dataclass(frozen=True)
class Return(Stmt):
    keywork: Token
    value: Expr | None
    
    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_return_stmt(self)

@dataclass(frozen=True)
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt | None  # else statements are optional, ya know!

    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_if_stmt(self)

@dataclass(frozen=True)
class While(Stmt):
    condition: Expr
    body: Stmt

    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_while_stmt(self)

@dataclass(frozen=True)
class Break(Stmt):
    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_break_stmt(self)

@dataclass(frozen=True)
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_var_stmt(self)

@dataclass(frozen=True)
class Block(Stmt):
    statements: list[Stmt]

    def accept[T](self, visitor: Stmt.Visitor[T]) -> T:
        return visitor.visit_block_stmt(self)
