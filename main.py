from enum import Enum

class TokenType(Enum):
    VARIABLE = 1

class Token:
    def __init__(self, token_type: TokenType, lexeme: str, line: int, column: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column

def tokenize() -> list[Token]:
    tokens = []
    
    tokens.append(Token(TokenType.VARIABLE, "x", 1, 1))

    return tokens

print(tokenize())