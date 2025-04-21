from lox.abcs.expr import (
    Expr,
    Binary,
    Grouping,
    Logical,
    Unary,
    Literal,
    Variable,
    Assign,
    Call,
    Get,
    Set,
    This,
)
from lox.abcs.stmt import (
    Stmt,
    Print,
    Function,
    Return,
    If,
    While,
    Expression,
    Var,
    Block,
    Break,
    Class
)
from lox.token.token import Token
from lox.interpreter import Interpreter
from lox.exceptions.errors import LoxException
from lox.abcs.stmt import Break
from lox.enums.functiontype import FunctionType
from lox.abcs.stmt import Class

scope = dict[str, bool]

class Resolver(Stmt.Visitor[None], Expr.Visitor[None]):
    """
    Resolver to walk through the syntrax tree before 
    interpreting.
    """

    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes: list[scope] = []  # Stack of scopes.
        self.current_function: FunctionType = FunctionType.NONE

    def resolve(self, *stmts: Stmt | Expr) -> None:
        for statement in stmts:
            statement.accept(self)

    def resolve_function(
            self,
            function: Function,
            functiontype: FunctionType
    ) -> None:
        enclosing_function = self.current_function
        self.current_function = functiontype

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(*function.body)
        self.end_scope()

        self.current_function = enclosing_function

    def begin_scope(self) -> None:
        self.scopes.append({})

    def end_scope(self) -> None:
        self.scopes.pop()

    def declare(self, name: Token) -> None:
        if not self.scopes:
            return

        scope = self.scopes[-1]  # Peeking!

        if name.lexeme in self.scopes:
            raise LoxException(
                "Already a variable with that name in this scope"
            )

        scope[name.lexeme] = False

    def define(self, name: Token) -> None:
        if not self.scopes:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token) -> None:
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(
                    expr,
                    len(self.scopes) - 1 - i,
                )
                return

    def visit_block_stmt(self, stmt: Block) -> None:
        self.begin_scope()
        self.resolve(*stmt.statements)
        self.end_scope()

    def visit_class_stmt(self, stmt: Class) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)

        self.begin_scope()
        self.scopes[-1]["this"] = True
    
        for method in stmt.methods:
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            else:
                declaration = FunctionType.METHOD
            self.resolve_function(method, declaration)

        self.end_scope()

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.resolve(stmt.expression)

    def visit_function_stmt(self, stmt: Function) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)
    
    def visit_if_stmt(self, stmt: If) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)

        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visit_print_stmt(self, stmt: Print) -> None:
        self.resolve(stmt.expression)

    # TODO: Add equivalent for break statements.
    def visit_return_stmt(self, stmt: Return) -> None:
        if self.current_function == FunctionType.NONE:
            raise LoxException("Unexpected return statement")

        if stmt.value is not None:
            if self.current_function == FunctionType.INITIALIZER:
                raise LoxException(
                    stmt.keyword,
                    "Can't return a value from an initializer",    
                )
            self.resolve(stmt.value)

    def visit_break_stmt(self, stmt: Break) -> None:
        return None

    def visit_var_stmt(self, stmt: Var) -> None:
        self.declare(stmt.name)
        if stmt.initializer != None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def visit_while_stmt(self, stmt: While) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visit_assign_expr(self, expr: Assign) -> None:
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)
        return

    def visit_binary_expr(self, expr: Binary) -> None:
        self.resolve(expr.left, expr.right)

    def visit_call_expr(self, expr: Call) -> None:
        self.resolve(expr.callee)
        self.resolve(*expr.arguments)

    def visit_get_expr(self, expr: Get) -> None:
        self.resolve(expr.obj)

    def visit_grouping_expr(self, expr: Grouping) -> None:
        self.resolve(expr.expression)

    def visit_literal_expr(self, expr: Literal) -> None:
        return None

    def visit_logical_expr(self, expr: Logical) -> None:
        self.resolve(expr.left, expr.right)

    def visit_set_expr(self, expr: Set) -> None:
        self.resolve(expr.value)
        self.resolve(expr.obj)

    def visit_this_expr(self, expr: This) -> None:
        self.resolve_local(expr, expr.keyword)

    def visit_unary_expr(self, expr: Unary) -> None:
        self.resolve(expr.right)

    def visit_variable_expr(self, expr: Variable) -> None:
        if (
            self.scopes
            and expr.name.lexeme in self.scopes[-1] 
            and not self.scopes[-1][expr.name.lexeme]
        ):
            raise LoxException(
                """
                Can't read name in 
                it's own initializer
                """
            )

        self.resolve_local(expr, expr.name)
