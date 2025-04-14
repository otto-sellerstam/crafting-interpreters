from lox.token import Token
from lox.tokentype import TokenType
from lox.expr import Expr, Binary, Grouping, Logical, Unary, Literal, Variable, Assign, Call
from lox.stmt import Stmt, Print, If, While, Expression, Var, Block, Break
from lox.errors import LoxSyntaxError, LoxArgumentError

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def expression(self) -> Expr:
        return self.assignment()

    def declaration(self) -> Stmt:
        if self.match_tokentype(TokenType.VAR):
            return self.var_declaration()
                #    
        return self.statement()
        #try:
        #    if self.match_tokentype(TokenType.VAR):
        #        return self.var_declaration()
        #    
        #    return self.statement()
        #except:
        #    self.synchronize()
        #    return None

    def statement(self) -> Stmt:
        if self.match_tokentype(TokenType.PRINT):
            return self.print_statement()
        elif self.match_tokentype(TokenType.LEFT_BRACE):
            return Block(self.block())
        elif self.match_tokentype(TokenType.IF):
            return self.if_statement()
        elif self.match_tokentype(TokenType.WHILE):
            return self.while_statement()
        elif self.match_tokentype(TokenType.FOR):
            return self.for_statement()
        elif self.match_tokentype(TokenType.BREAK):
            return self.break_statement()
        
        return self.expression_statement()
    
    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition")

        then_branch = self.statement()
        else_branch = None
        if self.match_tokentype(TokenType.ELSE):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition")

        body = self.statement()

        return While(condition, body)
    
    def for_statement(self) -> Stmt:
        '''
        Instead of creating a new node type for our AST, we conver a for loop into
        a while loop. This means that the interpreter doesn't even need to be touched!
        The parser takes care of it all, almost like magic.
        '''
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'")

        initializer: None | Stmt
        if self.match_tokentype(TokenType.SEMICOLON):
            initializer = None
        elif self.match_tokentype(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition: None | Expr
        if self.match_tokentype(TokenType.SEMICOLON):
            condition = None
        else:
            condition = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition")

        increment: None | Expr
        if self.match_tokentype(TokenType.SEMICOLON):
            increment = None
        else:
            increment = self.expression()

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses")

        body = self.statement()

        # If there is an increment, run it after body.
        if increment is not None:
            body = Block([
                body,
                Expression(increment),
            ])

        # Create a while loop from condition and body.
        if condition is None:
            condition = Literal(True)
        body = While(condition, body)

        # Lastly, run the initializer before the previously constructed while loop.
        if initializer is not None:
            body = Block([
                initializer,
                body,
            ])

        return body
    
    def break_statement(self) -> Stmt:
        self.consume(TokenType.SEMICOLON, "Expect ';' after break statement.")
        return Break()

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
        expr = self.logical_or()

        if self.match_tokentype(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            # TODO: raise an error
            print(equals, 'Invalid assignment target')

        return expr
    
    def logical_or(self) -> Expr:
        expr = self.logical_and()

        while self.match_tokentype(TokenType.OR):
            operator = self.previous()
            right = self.logical_and()
            expr = Logical(expr, operator, right)

        return expr

    def logical_and(self) -> Expr:
        expr = self.equality()

        while self.match_tokentype(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

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

        return self.call()

    def finish_call(self, callee: Expr) -> Expr:
        arguments: list[Expr] = []

        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match_tokentype(TokenType.COMMA):
                if len(arguments) >= 255:  # For equivalence to bytecode VM.
                    raise LoxArgumentError('More than 255 function arguments not supported')
                arguments.append(self.expression())

        paren = self.consume(
            TokenType.RIGHT_PAREN,
            "Expect ')' after arguments",
        )

        return Call(callee, arguments, paren)

    def call(self) -> Expr:
        expr = self.primary()

        while True:
            if self.match_tokentype(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break

        return expr

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

        raise LoxSyntaxError('LoxSyntaxError: ' + message) # TODO: Fix.

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