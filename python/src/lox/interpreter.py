from typing import Any, Final
from collections import defaultdict

from lox.token.token import Token
from lox.enums.tokentype import TokenType
from lox.abcs.expr import Expr, Binary, Grouping, Literal, Logical, Unary, Variable, Assign, Call
from lox.abcs.stmt import Block, Stmt, Expression, If, Print, Var, While, Break, Function, Return
from lox.namespace import Namespace
from lox.abcs.lox_callable import LoxCallable
from lox.callables.lox_function import LoxFunction
from lox.callables.lox_class import LoxClass, LoxInstance
from lox.lox_globals.clock import Clock
from lox.exceptions.errors import LoxTypeError, LoxException
from lox.control_flow_exceptions.return_exception import Return as ReturnException
from lox.control_flow_exceptions.break_exception import Break as BreakException
from lox.abcs.stmt import Class
from python.src.lox.abcs.expr import Get, Set

class Interpreter(Expr.Visitor[Any], Stmt.Visitor[None]):

    lox_globals: Final = Namespace()
    namespace = lox_globals  # Changes depending on scope.
    locals: defaultdict[Expr, int | None]

    def __init__(self):
        self.lox_globals['clock'] = Clock()
        self.locals = defaultdict(lambda: None)

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        #except TypeError as e:
        #    print("The following Python error occured: ", e)
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

    def visit_get_expr(self, expr: Get) -> Any:
        obj = self.evaluate(expr.obj)

        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)

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

    def visit_set_expr(self, expr: Set) -> Any:
        obj = self.evaluate(expr.obj)

        if not isinstance(obj, LoxInstance):
            raise LoxException(
                "Only instances have fields!"
            )
        
        value = self.evaluate(expr.value)
        obj.set(expr.name, value)
        return value

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
        return self.look_up_variable(expr.name, expr)

    def look_up_variable(self, name: Token, expr: Expr) -> Any:
        distance = self.locals[expr]

        if distance is not None:
            ancestor = self.namespace.ancestor(distance)
            return ancestor[name.lexeme]
        else:
            return self.lox_globals[name.lexeme]

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth

    def execute_block(self, stmts: list[Stmt], namespace: Namespace):
        previous = self.namespace
        try:
            self.namespace = namespace

            for stmt in stmts:
                self.execute(stmt)
        finally:
            self.namespace = previous

    def visit_block_stmt(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Namespace(self.namespace))

    def visit_class_stmt(self, stmt: Class) -> None:
        # First setting None lets us reference the class inside itself.
        self.namespace[stmt.name.lexeme] = None
        klass = LoxClass(stmt.name.lexeme)
        self.namespace[stmt.name.lexeme] = klass

    def visit_expression_stmt(self, stmt: Expression) -> None:
        value = self.evaluate(stmt.expression)
        #print(value)

    def visit_function_stmt(self, stmt: Function) -> None:
        function = LoxFunction(stmt, self.namespace)
        self.namespace[stmt.name.lexeme] = function

        return None

    def visit_if_stmt(self, stmt: If) -> None:
        value = self.evaluate(stmt.condition)

        if value:
            self.execute(stmt.then_branch)
        else:
            if stmt.else_branch is not None:
                self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: While) -> None:
        while self.evaluate(stmt.condition):
            try:
                self.execute(stmt.body)
            except BreakException:
                break

    def visit_break_stmt(self, stmt: Break) -> None:
        raise BreakException 

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

        self.namespace[stmt.name.lexeme] = value

    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)

        distance = self.locals[expr]

        if distance is not None:
            ancestor = self.namespace.ancestor(distance)
            ancestor.assign(expr.name.lexeme, value)
        else:
            self.lox_globals.assign(expr.name.lexeme, value)

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