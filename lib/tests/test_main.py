from typing import List
from lib.lexical.lexical import Lexical, Token, TokenType, StringError, InvalidNumberError
import pytest

def tokens(filename: str, expected: List[Token]):
    lexer = Lexical(filename)
    
    result = lexer.tokenize()
    
    assert len(expected) == len(result), f"Expected {len(expected)} tokens, got {len(result)}"
    
    for i, token in enumerate(result):
        assert token == expected[i], f"Expected: {lexer.print_token(expected[i])}\nGot: {lexer.print_token(token)}"

def test_reserved_word_token():
    filename = "./lib/tests/files/reserved_words.pas"

    expected: List[Token] = [
        Token(TokenType.RESERVED_WORD_PROGRAM, "program", 0, 0),
        Token(TokenType.RESERVED_WORD_VAR, "var", 1, 0),
        Token(TokenType.RESERVED_WORD_INTEGER, "integer", 2, 0),
        Token(TokenType.RESERVED_WORD_REAL, "real", 3, 0),
        Token(TokenType.RESERVED_WORD_STRING, "string", 4, 0),
        Token(TokenType.RESERVED_WORD_BEGIN, "begin", 5, 0),
        Token(TokenType.RESERVED_WORD_END, "end", 6, 0),
        Token(TokenType.RESERVED_WORD_FOR, "for", 7, 0),
        Token(TokenType.RESERVED_WORD_TO, "to", 8, 0),
        Token(TokenType.RESERVED_WORD_WHILE, "while", 9, 0),
        Token(TokenType.RESERVED_WORD_DO, "do", 10, 0),
        Token(TokenType.RESERVED_WORD_BREAK, "break", 11, 0),
        Token(TokenType.RESERVED_WORD_CONTINUE, "continue", 12, 0),
        Token(TokenType.RESERVED_WORD_IF, "if", 13, 0),
        Token(TokenType.RESERVED_WORD_ELSE, "else", 14, 0),
        Token(TokenType.RESERVED_WORD_THEN, "then", 15, 0),
        Token(TokenType.RESERVED_WORD_WRITE, "write", 16, 0),
        Token(TokenType.RESERVED_WORD_WRITELN, "writeln", 17, 0),
        Token(TokenType.RESERVED_WORD_READ, "read", 18, 0),
        Token(TokenType.RESERVED_WORD_READLN, "readln", 19, 0),
    ]
    
    tokens(filename, expected)


def test_string_tokens():
    filename = "./lib/tests/files/string.pas"

    expected: List[Token] = [
        Token(TokenType.RESERVED_WORD_PROGRAM, "program", 0, 0),
        Token(TokenType.VARIABLE, "HelloWorld", 0, 8),
        Token(TokenType.RESERVED_WORD_BEGIN, "begin", 2, 0),
        
        Token(TokenType.STRING, '"Hello World!"', 3, 2),
        Token(TokenType.STRING, '"a\nb"', 4, 2),
        Token(TokenType.STRING, '"a\rb"', 5, 2),
        Token(TokenType.STRING, '"a\tb"', 6, 2),
        Token(TokenType.STRING, '"a\0b"', 7, 2),

        Token(TokenType.RESERVED_WORD_END, "end", 8, 0),
    ]
    
    tokens(filename, expected)
    

def test_string_error():
    filename = "./lib/tests/files/string_error.pas"

    lexer = Lexical(filename)
    
    with pytest.raises(StringError) as excinfo:
        lexer.tokenize()
    

def test_numbers():
    filename = "./lib/tests/files/numbers.pas"
        
    expected: List[Token] = [
        Token(TokenType.HEXADECIMAL, "0x1A", 0, 0),
        Token(TokenType.DECIMAL, "10", 1, 0),
        Token(TokenType.FLOAT, "1.54", 2, 0),
        Token(TokenType.OCTAL, "07", 3, 0),
        Token(TokenType.FLOAT, "0.5", 4, 0),
        Token(TokenType.FLOAT, "1.0", 5, 0),
        
        Token(TokenType.DECIMAL, "8", 7, 0),
        Token(TokenType.OPERATOR_LESS_EQUAL, "<=", 7, 1),

        Token(TokenType.FLOAT, "89.123", 7, 4),
        Token(TokenType.OPERATOR_GREATER, ">", 7, 10),

        Token(TokenType.OCTAL, "06", 7, 12),
        Token(TokenType.OPERATOR_ASSIGN, ":=", 7, 14),

        Token(TokenType.HEXADECIMAL, "0xFFF", 7, 17),
        Token(TokenType.SEMICOLON, ";", 7, 22),

        Token(TokenType.FLOAT, "1.0", 7, 24),
        Token(TokenType.SEMICOLON, ";", 7, 26),

        Token(TokenType.DECIMAL, "7", 8, 0),

        Token(TokenType.FLOAT, "4321.123", 8, 2),

        Token(TokenType.OCTAL, "01", 8, 11),

        Token(TokenType.HEXADECIMAL, "0xA", 8, 14),

        Token(TokenType.FLOAT, "1.0", 8, 18),
    ]
    
    tokens(filename, expected)
    
        
@pytest.mark.parametrize("filename", [
    "./lib/tests/files/number_error1.pas",
    "./lib/tests/files/number_error2.pas",
    "./lib/tests/files/number_error3.pas",
    "./lib/tests/files/number_error4.pas",
])
def test_invalid_number_errors(filename):
    lexer = Lexical(filename)
    
    with pytest.raises(InvalidNumberError) as excinfo:
        lexer.tokenize()
        
        
def test_equal():
    filename = "./lib/tests/files/equal.pas"
        
    expected: List[Token] = [
        Token(TokenType.OPERATOR_EQUAL, "=", 0, 0),
        Token(TokenType.OPERATOR_EQUAL, "==", 1, 0),
        Token(TokenType.OPERATOR_EQUAL, "==", 2, 0),
        Token(TokenType.OPERATOR_EQUAL, "=", 2, 2)
    ]
    
    tokens(filename, expected)
    

def test_operators():
    filename = "./lib/tests/files/operators.pas"
        
    expected: List[Token] = [
        Token(TokenType.OPERATOR_PLUS, "+", 0, 0),
        Token(TokenType.OPERATOR_MINUS, "-", 1, 0),
        Token(TokenType.OPERATOR_MULTIPLY, "*", 2, 0),
        Token(TokenType.OPERATOR_DIVIDE, "/", 3, 0),
        
        Token(TokenType.OPERATOR_MOD, "mod", 4, 0),
        Token(TokenType.OPERATOR_INTEGER_DIVIDER, "div", 5, 0),
        Token(TokenType.OPERATOR_OR, "or", 6, 0),
        Token(TokenType.OPERATOR_AND, "and", 7, 0),
        Token(TokenType.OPERATOR_NOT, "not", 8, 0),
        
        Token(TokenType.OPERATOR_EQUAL, "=", 9, 0),
        Token(TokenType.OPERATOR_EQUAL, "==", 10, 0),
        Token(TokenType.OPERATOR_NOT_EQUAL, "<>", 11, 0),
        Token(TokenType.OPERATOR_GREATER, ">", 12, 0),
        Token(TokenType.OPERATOR_GREATER_EQUAL, ">=", 13, 0),
        Token(TokenType.OPERATOR_LESS, "<", 14, 0),
        Token(TokenType.OPERATOR_LESS_EQUAL, "<=", 15, 0),
        Token(TokenType.OPERATOR_ASSIGN, ":=", 16, 0)
    ]
    
    tokens(filename, expected)
    
def test_symbols():
    filename = "./lib/tests/files/symbols.pas"
        
    expected: List[Token] = [
        Token(TokenType.SEMICOLON, ";", 0, 0),
        Token(TokenType.COMMA, ",", 1, 0),
        Token(TokenType.DOT, ".", 2, 0),
        Token(TokenType.COLON, ":", 3, 0),
        Token(TokenType.OPEN_PARENTHESES, "(", 4, 0),
        Token(TokenType.CLOSE_PARENTHESES, ")", 5, 0),
    ]
    
    tokens(filename, expected)