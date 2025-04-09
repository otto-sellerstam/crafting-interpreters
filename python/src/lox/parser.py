from lox.token import Token
from lox.tokentype import TokenType
from lox.expr import Expr, Binary, Grouping, Unary, Literal

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(
            TokenType.BANG_EQUAL,
            TokenType.EQUAL_EQUAL,
        ):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(
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

        while self.match(
            TokenType.MINUS,
            TokenType.PLUS,
        ):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(
            TokenType.SLASH,
            TokenType.STAR,
        ):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(
            TokenType.BANG,
            TokenType.MINUS,
        ):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN,
                "Expected '(' after expression."    
            )
            return Grouping(expr)

        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)

        if self.match(
            TokenType.NUMBER,
            TokenType.STRING,
        ):
            return Literal(self.previous().literal)

        #throw error(peek(), "Expected expression.")

    def match(self, *tokentypes: TokenType) -> bool:
        for tokentype in tokentypes:
            if self.check(tokentype):
                self.advance()
                return True
            
        return False

    def consume(self, tokentype: TokenType, message: str) -> Token:
        if self.check(tokentype):
            return self.advance()

        #throw error(peek(), message);

    def synchronize(self):
        self.advance()

        while not self.isatend():
            if self.previous().tokentype == TokenType.SEMICOLON:
                return

            if self.peek().tokentype in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self.advance()

    def check(self, tokentype: TokenType) -> bool:
        if self.isatend():
            return False

        return self.peek().tokentype == tokentype

    def advance(self) -> Token:
        if not self.isatend():
            self.current += 1

        return self.previous()

    def isatend(self) -> bool:
        return self.peek().tokentype == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def parse(self) -> Expr:
        try:
            return self.expression()
        except Exception as e:
            print(f'An error occurred during parsing: {e}')
            raise e
            return None
