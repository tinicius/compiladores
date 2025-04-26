from lexical.token_type import TokenType


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