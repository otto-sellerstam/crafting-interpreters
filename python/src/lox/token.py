from dataclasses import dataclass
from typing import Any

from lox.tokentype import TokenType

@dataclass
class Token:
    tokentype: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self) -> str:
        return self.tokentype + ' ' + self.lexeme + ' ' + self.literal
