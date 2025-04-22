from typing import List
from src.main import Lexical, Token, TokenType

def test_reserved_word_token():
    filename = "./examples/reserved_words.pas"

    lexer = Lexical(filename)

    expected: List[Token] = [
        Token(TokenType.RESERVED_WORD_PROGRAM, "program", 0, 0),
        Token(TokenType.VARIABLE, "HelloWorld", 0, 8),
        Token(TokenType.RESERVED_WORD_BEGIN, "begin", 2, 0),
        Token(TokenType.RESERVED_WORD_VAR, "var", 3, 2),
        Token(TokenType.RESERVED_WORD_INTEGER, "integer", 4, 2),
        Token(TokenType.RESERVED_WORD_REAL, "real", 5, 2),
        Token(TokenType.RESERVED_WORD_STRING, "string", 6, 2),
        Token(TokenType.RESERVED_WORD_END, "end", 7, 2),
        Token(TokenType.RESERVED_WORD_FOR, "for", 8, 2),
        Token(TokenType.RESERVED_WORD_TO, "to", 9, 2),
        Token(TokenType.RESERVED_WORD_WHILE, "while", 10, 2),
        Token(TokenType.RESERVED_WORD_DO, "do", 11, 2),
        Token(TokenType.RESERVED_WORD_BREAK, "break", 12, 2),
        Token(TokenType.RESERVED_WORD_CONTINUE, "continue", 13, 2),
        Token(TokenType.RESERVED_WORD_IF, "if", 14, 2),
        Token(TokenType.RESERVED_WORD_ELSE, "else", 15, 2),
        Token(TokenType.RESERVED_WORD_THEN, "then", 16, 2),
        Token(TokenType.RESERVED_WORD_WRITE, "write", 17, 2),
        Token(TokenType.RESERVED_WORD_WRITELN, "writeln", 18, 2),
        Token(TokenType.RESERVED_WORD_READ, "read", 19, 2),
        Token(TokenType.RESERVED_WORD_READLN, "readln", 20, 2),
        Token(TokenType.RESERVED_WORD_END, "end", 21, 0),
    ]
    
    assert lexer.tokenize() == expected


def test_string_tokens():
    filename = "./examples/string.pas"

    lexer = Lexical(filename)

    expected: List[Token] = [
        Token(TokenType.RESERVED_WORD_PROGRAM, "program", 0, 0),
        Token(TokenType.VARIABLE, "HelloWorld", 0, 8),
        Token(TokenType.RESERVED_WORD_BEGIN, "begin", 2, 0),
        
        Token(TokenType.STRING, '"Hello World!"', 3, 2),
        Token(TokenType.STRING, '"Linha1\nLinha2"', 4, 2),

        Token(TokenType.RESERVED_WORD_END, "end", 5, 0),
    ]
    
    assert lexer.tokenize() == expected