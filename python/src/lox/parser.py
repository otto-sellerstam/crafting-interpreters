from lox.token import Token
from lox.tokentype import TokenType
from lox.expr import Expr, Binary, Grouping, Unary, Literal, Variable, Assign
from lox.stmt import Stmt, Print, Expression, Var, Block

class LoxSyntaxError(SyntaxError):
    pass

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def expression(self) -> Expr:
        return self.assignment()

    def declaration(self) -> Stmt:
        try:
            if self.match_tokentype(TokenType.VAR):
                return self.var_declaration()
            
            return self.statement()
        except:
            self.synchronize()
            return None

    def statement(self) -> Stmt:
        if self.match_tokentype(TokenType.PRINT):
            return self.print_statement()
        if self.match_tokentype(TokenType.LEFT_BRACE):
            return Block(self.block())
        
        return self.expression_statement()

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer: Expr | None = None
        if self.match_tokentype(TokenType.EQUAL):
            initializer = self.expression()

        if initializer is None: # Not sure about this...
            initializer = Literal(None)
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Var(name, initializer)

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(expr)
    
    def block(self) -> list[Stmt]:
        statements: list[Stmt] = []

        while (
            not self.check(TokenType.RIGHT_BRACE)
            and not self.isatend()
        ):
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block")
        return statements

    def assignment(self) -> Expr:
        expr = self.equality()

        if self.match_tokentype(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            # TODO: raise an error
            print(equals, 'Invalid assignment target')

        return expr

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match_tokentype(
            TokenType.BANG_EQUAL,
            TokenType.EQUAL_EQUAL,
        ):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match_tokentype(
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

        while self.match_tokentype(
            TokenType.MINUS,
            TokenType.PLUS,
        ):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match_tokentype(
            TokenType.SLASH,
            TokenType.STAR,
        ):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match_tokentype(
            TokenType.BANG,
            TokenType.MINUS,
        ):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match_tokentype(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match_tokentype(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN,
                "Expected '(' after expression."    
            )
            return Grouping(expr)

        if self.match_tokentype(TokenType.FALSE): return Literal(False)
        if self.match_tokentype(TokenType.TRUE): return Literal(True)
        if self.match_tokentype(TokenType.NIL): return Literal(None)

        if self.match_tokentype(
            TokenType.NUMBER,
            TokenType.STRING,
        ):
            return Literal(self.previous().literal)

        raise LoxSyntaxError # Ideall

        #throw error(peek(), "Expected expression.")

    def match_tokentype(self, *tokentypes: TokenType) -> bool:
        for tokentype in tokentypes:
            if self.check(tokentype):
                self.advance()
                return True
            
        return False

    def consume(self, tokentype: TokenType, message: str) -> Token:
        if self.check(tokentype):
            return self.advance()

        raise Exception # TODO: Fix.

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

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.isatend():
            statements.append(self.declaration())
        
        return statements