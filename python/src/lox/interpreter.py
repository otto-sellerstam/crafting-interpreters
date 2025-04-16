from typing import Any, Final

from lox.tokentype import TokenType
from lox.expr import Expr, Binary, Grouping, Literal, Logical, Unary, Variable, Assign, Call
from lox.stmt import Block, Stmt, Expression, If, Print, Var, While, Break, Function, Return
from lox.namespace import Namespace
from lox.lox_callable import LoxCallable
from lox.lox_function import LoxFunction
from lox.lox_globals import Clock
from lox.errors import LoxTypeError
from lox.return_exception import Return as ReturnException

class Interpreter(Expr.Visitor[Any], Stmt.Visitor[None]):

    lox_globals: Final = Namespace()
    namespace = lox_globals  # Changes depending on scope.
    break_detected = False

    def __init__(self):
        self.lox_globals.define(
            'clock',
            Clock(),
        )

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except TypeError as e:
            print("The following Python error occured: ", e)
        except ZeroDivisionError:
            print("Division by zero not allowed! Bad stuff might happen...")

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
                return left + right  # No special string handling. Yeah baby!

        return None

    def visit_call_expr(self, expr: Call) -> Any:
        callee = self.evaluate(expr.callee)

        arguments = [self.evaluate(argument) for argument in expr.arguments]

        function: LoxCallable = callee

        if len(arguments) != function.arity():
            raise LoxTypeError(
                f'Expected {function.arity()} arguments but got {len(arguments)}'
            )

        try:
            call_value = function.call(self, arguments)
        except TypeError:
            raise LoxTypeError('Can only call functions and classes')

        return call_value

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
    
    def visit_logical_expr(self, expr: Logical) -> Any:
        left_value = self.evaluate(expr.left)

        if expr.operator.tokentype == TokenType.OR:
            if left_value:
                return True
        elif expr.operator.tokentype == TokenType.AND:
            if not left_value:
                return False

        return self.evaluate(expr.right)

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
        return self.namespace.get(expr.name)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def execute_block(self, stmts: list[Stmt], namespace: Namespace):
        previous = self.namespace
        try:
            self.namespace = namespace

            for stmt in stmts:
                self.execute(stmt)
                if self.break_detected:
                    break
        finally:
            self.namespace = previous

    def visit_block_stmt(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Namespace(self.namespace))

    def visit_expression_stmt(self, stmt: Expression) -> None:
        value = self.evaluate(stmt.expression)
        #print(value)

    def visit_function_stmt(self, stmt: Function) -> None:
        function = LoxFunction(stmt)
        self.namespace.define(
            stmt.name.lexeme,
            function,
        )

        return None

    def visit_if_stmt(self, stmt: If) -> None:
        value = self.evaluate(stmt.condition)

        if value:
            self.execute(stmt.then_branch)
        else:
            if stmt.else_branch is not None:
                self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: While) -> None:
        while self.evaluate(stmt.condition) and not self.break_detected:
            self.execute(stmt.body)
        self.break_detected = False

    def visit_break_stmt(self, stmt: Break) -> None:
        self.break_detected = True 

    def visit_print_stmt(self, stmt: Print) -> None:
        ''' Same as above, but we don't discard the value but print it. '''
        value = self.evaluate(stmt.expression)
        print(value)

    def visit_return_stmt(self, stmt: Return) -> None:
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        
        # We raise an Exception for control flow to unwind the interpeter stack to
        # to the corresponding function call.
        raise ReturnException(value)

    def visit_var_stmt(self, stmt: Var) -> None:
        value = None

        if (stmt.initializer is not None):
            value = self.evaluate(stmt.initializer)

        self.namespace.define(stmt.name.lexeme, value)

    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)
        self.namespace.assign(expr.name, value)
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