
import logging

from python.src.lox.scanner import Scanner
from python.src.lox.token import Token
from python.src.lox.tokentype import TokenType

logger = logging.getLogger(__name__)

class Lox:
    had_error: bool = False

    def run(source: str):
        scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def run_file(path: str):
        pass

    def run_prompt():
        pass

    def error(
        self,
        token: Token,
        message: str,
        line: int | None = None,
    ):
        if line is None:
            self.report(line, '', message)
        else:
            if (token.type == TokenType.EOF):
                self.report(token.line, ' at end', message)
            else:
                self.report(token.line, ' at \'' + token.lexeme + '\'', message)

    def report(
        self,
        line: int,
        where: str,
        message: str,
    ):
        logger.error("[line " + line + "] Error" + where + ": " + message)
        self.had_error = True
