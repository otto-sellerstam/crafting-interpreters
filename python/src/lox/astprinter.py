from lox.expr import Visitor, Expr, Binary, Grouping, Literal, Unary
from lox.token import Token
from lox.tokentype import TokenType

class AstPrinter(Visitor[str]):

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(
            expr.operator.lexeme,
            expr.left,
            expr.right,
        )

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize(
            "group",
            expr.expression,
        )

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(
            expr.operator.lexeme,
            expr.right,
        )

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        #builder = ''
        #
        #builder += '('
        #builder += name
        #
        #for expr in exprs:
        #    builder += ' '
        #    builder += expr.accept(self)
        #
        #builder += ')'

        builder = f'({name} {" ".join(expr.accept(self) for expr in exprs)})'
        return builder

if __name__ == '__main__':
    expression = Binary(
        Binary(
            Literal(2),
            Token(TokenType.PLUS, '+', None, 1),
            Literal(3),
        ),
        Token(TokenType.STAR, '*', None, 1),
        Grouping(
            Binary(
                Literal(5),
                Token(TokenType.MINUS, '-', None, 1),
                Literal(1),
            )
        )
    )

    print(AstPrinter().print(expression))
