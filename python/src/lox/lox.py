
from python.src.lox.scanner import Scanner
from python.src.lox.token import Token

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

    def error():
        pass

    def report():
        pass