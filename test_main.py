from typing import List
from main import tokenize, Token, TokenType

def test_token():
    file = "example.pas"

    expected: List[Token] = [
        Token(TokenType.RESERVED_WORD_PROGRAM, "program", 0, 0),
        Token(TokenType.VARIABLE, "HelloWorld", 0, 8),
        Token(TokenType.SEMICOLON, ";", 0, 20),
        Token(TokenType.RESERVED_WORD_BEGIN, "begin", 2, 0),
        Token(TokenType.VARIABLE, "writeln", 3, 2),
        Token(TokenType.OPEN_PARENTHESES, "(", 3, 9),
        Token(TokenType.STRING, '"Hello, World!"', 3, 10),
        Token(TokenType.CLOSE_PARENTHESES, ")", 3, 25),
        Token(TokenType.SEMICOLON, ";", 3, 26),
        Token(TokenType.RESERVED_WORD_END, "end.", 4, 0),
        Token(TokenType.DOT, ".", 4, 3),
    ]
    
    assert tokenize(file) == expected
