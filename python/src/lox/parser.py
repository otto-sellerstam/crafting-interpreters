from python.src.lox.token import Token
from python.src.lox.expr import Expr, Binary, Grouping, Unary, Literal

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while match(
            TokenType.BANG_EQUAL,
            TokenType.EQUAL_EQUAL,
        ):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while match(
            TokenType.MINUS,
            TokenType.PLUS,
        ):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while match(
            TokenType.SLASH,
            TokenType.STAR,
        ):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if match(
            TokenType.BANG,
            TokenType.MINUS,
        ):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN,
                "Expected '(' after expression."    
            )
            return Grouping(expr)

        if self.match(TokenType.FALSE) return Literal(False)
        if self.match(TokenType.TRUE) return Literal(True)
        if self.match(TokenType.NIL) return Literal(None)

        if self.match(
            TokenType.NUMBER,
            TokenType.STRING,
        ):
            return Literal(previous().literal)

        #throw error(peek(), "Expected expression.")

    

