
import logging

from lox.scanner import Scanner
from lox.token import Token
from lox.tokentype import TokenType
from lox.parser import Parser
from lox.astprinter import AstPrinter

logger = logging.getLogger(__name__)

class Lox:
    had_error: bool = False

    def run(self, source: str):
        print('Running with source', source)
        scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if self.had_error:
            return

        ast_printer = AstPrinter()
        print(ast_printer.print(expression))

    def run_file(self, path: str):
        pass

    def run_prompt(self):
        while True:
            line = input('> ')
            if line is None:
                break
            self.run(line)
            self.had_error = False

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

if __name__ == '__main__':
    Lox().run_prompt()