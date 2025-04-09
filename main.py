from enum import Enum

class TokenType(Enum):
    VARIABLE = 1
    RESERVED_WORD_PROGRAM = 2
    STRING = 3
    OPEN_PARENTHESES = 4
    CLOSE_PARENTHESES = 5
    SEMICOLON = 6

class Token:
    def __init__(self, token_type: TokenType, lexeme: str, line: int, column: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column

def tokenize(filename: str) -> list[Token]:
    tokens = []
    
    with open(filename, 'r') as file:

        for line in file:
            print(line.strip()) 

    return tokens
