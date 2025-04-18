from typing import Any

from lox.token.token import Token
from lox.enums.tokentype import TokenType
#from lox.lox import Lox

class Scanner:
    keywords: dict[str, TokenType] = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'for': TokenType.FOR,
        'fun': TokenType.FUN,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE,
        'break': TokenType.BREAK,
    }

    #keywords: dict[str, TokenType] = {
    #    'och': TokenType.AND,
    #    'klass': TokenType.CLASS,
    #    'annars': TokenType.ELSE,
    #    'falskt': TokenType.FALSE,
    #    'för': TokenType.FOR,
    #    'funktion': TokenType.FUN,
    #    'om': TokenType.IF,
    #    'ingenting': TokenType.NIL,
    #    'eller': TokenType.OR,
    #    'skriv': TokenType.PRINT,
    #    'retur': TokenType.RETURN,
    #    'super': TokenType.SUPER,
    #    'denna': TokenType.THIS,
    #    'sant': TokenType.TRUE,
    #    'grej': TokenType.VAR,
    #    'när': TokenType.WHILE,
    #    'sluta': TokenType.BREAK,
    #}

    def __init__(self, source: str):
        self.source: str = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.isatend():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        
        return self.tokens

    def scan_token(self):
        char: str = self.advance()
        match char:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('/'): # Single line comment.
                    while self.peek() != '\n' and not self.isatend():
                        self.advance()
                elif self.match('*'): # Multiline comment.
                    self.multiline_comment()
                else:
                    self.add_token(TokenType.SLASH)

            case ' ' | '\r' | '\t': pass # Ignore whitespaces
            case '\n':
                self.line += 1
            case '"': self.string()
            case _:
                if char.isdigit():
                    self.number()
                elif char.isalpha():
                    self.identifier()
                else:
                    pass
                    #Lox.error(self.line, 'Unexpected character.')

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        text = self.source[self.start:self.current]
        tokentype = self.keywords.get(text, None)
        if tokentype is None:
            tokentype = TokenType.IDENTIFIER

        self.add_token(tokentype)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        text = self.source[self.start:self.current]
        self.add_token(TokenType.NUMBER, float(text))

    def string(self):
        while self.peek() != '"' and not self.isatend():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.isatend():
            #Lox.error(self.line, "Unterminated string literal.")
            return

        self.advance()

        text = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, text)

    def multiline_comment(self):
        while (
            self.peek() != '*' 
            and self.peek_next() != '/'
            and not self.isatend()
        ):
            if self.advance() == '\n':
                self.line += 1

        if self.peek() == '*' and self.peek_next() == '/':
            self.advance()
            self.advance()
        elif self.isatend():
            #Lox.error(self.line, "Unterminated multiline comment.")
            return

    def match(self, expected: str) -> bool:
        if self.isatend():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.isatend():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def isatend(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        value = self.source[self.current]
        self.current += 1
        return value

    def add_token(
        self,
        tokentype: TokenType,
        literal: Any = None,
    ):
        text = self.source[self.start:self.current]
        self.tokens.append(
            Token(
                tokentype,
                text,
                literal,
                self.line,
            )
        )
