
import logging
import sys

from lox.scanner import Scanner
from lox.token.token import Token
from lox.enums.tokentype import TokenType
from lox.parser import Parser
from lox.astprinter import AstPrinter
from lox.interpreter import Interpreter
from lox.resolver import Resolver
from lox.exceptions.errors import LoxException

logger = logging.getLogger(__name__)

class Lox:
    had_error: bool = False

    def __init__(self):
        self.interpreter = Interpreter()
        self.resolver = Resolver(self.interpreter)

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        statements = parser.parse()

        if self.had_error:
            return
        
        self.resolver.resolve(*statements)
        self.interpreter.interpret(statements)

        #ast_printer = AstPrinter()
        #print(ast_printer.print(expression))

    def run_file(self, path: str):
        with open(path, 'r') as file:
            self.run(file.read())

        if self.had_error:
            sys.exit(65)

    def run_prompt(self):
        while True:
            line = input('> ')
            if line is None:
                break

            try:
                self.run(line)
            except LoxException as e:
                print(e)

            self.had_error = False

    def error(
        self,
        token: Token,
        message: str,
        line: int | None = None,
    ):
        if line is None:
            self.report(-1, '', message)
        else:
            if (token.tokentype == TokenType.EOF):
                self.report(token.line, ' at end', message)
            else:
                self.report(token.line, ' at \'' + token.lexeme + '\'', message)

    def report(
        self,
        line: int,
        where: str,
        message: str,
    ):
        logger.error('[line ' + str(line) + '] Error' + where + ': ' + message)
        self.had_error = True

if __name__ == '__main__':
    lox = Lox()

    if len(sys.argv) == 2:  # Assume second argument is file path.
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()