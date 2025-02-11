from . import mmciflexer as lex
from .parser import Parser
from .parser_flat import ParserFlat

__version__ = "0.6.2"

def print_version() -> None:
    print("--- mmcifbuddy ---")
    print(f"version: {__version__}")
    print("git branch:", lex.GIT_BRANCH)
    print("git commit:", lex.GIT_COMMIT)
    print("--- Lexer ---")
    print("compile time:", lex.COMPILE_TIME)
