from dataclasses import dataclass
from typing import Any

from lox.enums.tokentype import TokenType

@dataclass(frozen=True)
class Token:
    tokentype: TokenType
    lexeme: str
    literal: Any
    line: int
