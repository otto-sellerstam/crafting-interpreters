from lox.abcs.stmt import *
from lox.abcs.expr import *
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
        self.scopes: list[scope] = []  # We'll use as stack.
        self.current_function: FunctionType = FunctionType.NONE

    def resolve_stmt(self, stmts: list[Stmt]) -> None:
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
        self.resolve_stmt(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    def resolve_expr(self, exprs: list[Expr]) -> None:
        for expression in exprs:
            expression.accept(self)

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
        self.resolve_stmt(stmt.statements)
        self.end_scope()

    def visit_class_stmt(self, stmt: Class) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.resolve_expr([stmt.expression])

    def visit_function_stmt(self, stmt: Function) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)
    
    def visit_if_stmt(self, stmt: If) -> None:
        self.resolve_expr([stmt.condition])
        self.resolve_stmt([stmt.then_branch])

        if stmt.else_branch is not None:
            self.resolve_stmt([stmt.else_branch])

    def visit_print_stmt(self, stmt: Print) -> None:
        self.resolve_expr([stmt.expression])

    # TODO: Add equivalent for break statements.
    def visit_return_stmt(self, stmt: Return) -> None:
        if self.current_function == FunctionType.NONE:
            raise LoxException("Unexpected return statement")

        if stmt.value is not None:
            self.resolve_expr([stmt.value])

    def visit_break_stmt(self, stmt: Break) -> None:
        return None

    def visit_var_stmt(self, stmt: Var) -> None:
        self.declare(stmt.name)
        if stmt.initializer != None:
            self.resolve_expr([stmt.initializer])
        self.define(stmt.name)

    def visit_while_stmt(self, stmt: While) -> None:
        self.resolve_expr([stmt.condition])
        self.resolve_stmt([stmt.body])

    def visit_assign_expr(self, expr: Assign) -> None:
        self.resolve_expr([expr.value])
        self.resolve_local(expr, expr.name)
        return

    def visit_binary_expr(self, expr: Binary) -> None:
        self.resolve_expr([expr.left, expr.right])

    def visit_call_expr(self, expr: Call) -> None:
        self.resolve_expr([expr.callee])
        self.resolve_expr(expr.arguments)

    def visit_grouping_expr(self, expr: Grouping) -> None:
        self.resolve_expr([expr.expression])

    def visit_literal_expr(self, expr: Literal) -> None:
        return None

    def visit_logical_expr(self, expr: Logical) -> None:
        self.resolve_expr([expr.left, expr.right])

    def visit_unary_expr(self, expr: Unary) -> None:
        self.resolve_expr([expr.right])

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
