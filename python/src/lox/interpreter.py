from typing import Any

from lox.tokentype import TokenType
from lox.expr import Expr, Binary, Grouping, Literal, Unary, Variable, Assign
from lox.stmt import Block, Stmt, Expression, Print, Var
from lox.environment import Environment

class Interpreter(Expr.Visitor[Any], Stmt.Visitor[None]):

    environment = Environment()

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except TypeError as e:
            print("The following Python error occured: ", e)
        except ZeroDivisionError:
            print("Division by zero not allowed! Bad stuff might happen")

    def visit_binary_expr(self, expr: Binary) -> Any:
        """Process a binary expression.
        
        Args:
            expr: The binary expression to process.
        """
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.tokentype:
            # Comparison.
            case TokenType.GREATER:
                return left > right
            case TokenType.GREATER_EQUAL:
                return left >= right
            case TokenType.LESS:
                return left < right
            case TokenType.LESS_EQUAL:
                return left <= right
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right
            
            # Arithmetic.
            case TokenType.MINUS:
                return left - right
            case TokenType.SLASH:
                return left / right
            case TokenType.STAR:
                return left * right
            case TokenType.PLUS:
                return left + right # Don't think I need special string handling?

        return None

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        """Process a grouping expression.
        
        Args:
            expr: The grouping expression to process.
        """
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal) -> Any:
        """Process a literal expression.
        
        Args:
            expr: The literal expression to process.
        """
        return expr.value

    def visit_unary_expr(self, expr: Unary) -> Any:
        """Process a unary expression.
        
        Args:
            expr: The unary expression to process.
        """
        right = self.evaluate(expr.right)

        match expr.operator.tokentype:
            case TokenType.MINUS:
                return -right # TODO: Test. I don't think I need to convert to float?
            case TokenType.BANG:
                return not self.is_truthy(right)

        return None

    def visit_variable_expr(self, expr: Variable) -> Any:
        return self.environment.get(expr.name)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def execute_block(self, stmts: list[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment

            for stmt in stmts:
                self.execute(stmt)
        finally:
            self.environment = previous

    def visit_block_stmt(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression_stmt(self, stmt: Expression) -> None:
        value = self.evaluate(stmt.expression)
        print(value)

    def visit_print_stmt(self, stmt: Print) -> None:
        ''' Same as above, but we don't discard the value but print it. '''
        value = self.evaluate(stmt.expression)
        print(value)

    def visit_var_stmt(self, stmt: Var) -> None:
        value = None

        if (stmt.initializer is not None):
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def is_truthy(self, value: Any):
        '''
        Like in Ruby, everything except "false" and "nil" are truthy.
        '''
        if (value == None):
            return False
        
        if (isinstance(value, bool)):
            return value
        
        return False