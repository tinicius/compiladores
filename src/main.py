from enum import Enum, auto
from pathlib import Path


class TokenType(Enum):
    VARIABLE = auto()
    RESERVED_WORD_PROGRAM = auto()
    RESERVED_WORD_BEGIN = auto()
    RESERVED_WORD_END = auto()
    RESERVED_WORD_VAR = auto()
    RESERVED_WORD_INTEGER = auto()
    RESERVED_WORD_REAL = auto()
    RESERVED_WORD_STRING = auto()
    RESERVED_WORD_FOR = auto()
    RESERVED_WORD_TO = auto()
    RESERVED_WORD_WHILE = auto()
    RESERVED_WORD_DO = auto()
    RESERVED_WORD_BREAK = auto()
    RESERVED_WORD_CONTINUE = auto()
    RESERVED_WORD_IF = auto()
    RESERVED_WORD_ELSE = auto()
    RESERVED_WORD_THEN = auto()
    RESERVED_WORD_WRITE = auto()
    RESERVED_WORD_WRITELN = auto()
    RESERVED_WORD_READ = auto()
    RESERVED_WORD_READLN = auto()
    STRING = auto()
    OPEN_PARENTHESES = auto()
    CLOSE_PARENTHESES = auto()
    SEMICOLON = auto()
    DOT = auto()

class Token:
    def __init__(self, token_type: TokenType, lexeme: str, line: int, column: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.token_type == other.token_type and
                self.lexeme == other.lexeme and
                self.line == other.line and
                self.column == other.column)

token_map: dict[str, TokenType] = {
    "program": TokenType.RESERVED_WORD_PROGRAM,
    "var": TokenType.RESERVED_WORD_VAR,
    "integer": TokenType.RESERVED_WORD_INTEGER,
    "real": TokenType.RESERVED_WORD_REAL,
    "string": TokenType.RESERVED_WORD_STRING,
    "begin": TokenType.RESERVED_WORD_BEGIN,
    "end": TokenType.RESERVED_WORD_END,
    "for": TokenType.RESERVED_WORD_FOR,
    "to": TokenType.RESERVED_WORD_TO,
    "while": TokenType.RESERVED_WORD_WHILE,
    "do": TokenType.RESERVED_WORD_DO,
    "break": TokenType.RESERVED_WORD_BREAK,
    "continue": TokenType.RESERVED_WORD_CONTINUE,
    "if": TokenType.RESERVED_WORD_IF,
    "else": TokenType.RESERVED_WORD_ELSE,
    "then": TokenType.RESERVED_WORD_THEN,
    "write": TokenType.RESERVED_WORD_WRITE,
    "writeln": TokenType.RESERVED_WORD_WRITELN,
    "read": TokenType.RESERVED_WORD_READ,
    "readln": TokenType.RESERVED_WORD_READLN,
}

def get_tokens_from_line(line: str, line_i: int) -> list[Token]:
    tokens = []

    idx = 0
    start_idx = 0

    state = 0

    aux: str = ""

    while idx < len(line):
        match state:
            case 0:
                if line[idx].isalpha():
                    aux += line[idx]
                    idx += 1
                    state = 1
                else:
                    idx += 1
                    state = 0
                    start_idx = idx
            case 1:
                if line[idx].isalpha() or line[idx].isdigit():
                    aux += line[idx]
                    idx += 1
                    state = 1
                else:
                    idx += 1
                    if (token_map.get(aux) is not None):
                        tokens.append(Token(token_map[aux], aux, line_i, start_idx))
                    else:
                        tokens.append(Token(TokenType.VARIABLE, aux, line_i, start_idx))
                    
                    state = 0
                    start_idx = idx
                    aux = ""
                        
    return tokens

def print_token(token: Token):
    print(f"({token.token_type}, {token.lexeme}, {token.line}, {token.column})")

def tokenize(filename: str) -> list[Token]:
    tokens = []
    
    try:
        with open(filename, 'r') as file:

            for i, line in enumerate(file):

                line_tokens = get_tokens_from_line(line, i)
                for token in line_tokens:
                    tokens.append(token)
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")

    for token in tokens:
        print_token(token)

    return tokens
