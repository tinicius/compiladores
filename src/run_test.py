from main import Lexical, Token, TokenType, StringError
test_file = "../examples/test.pas"

lexer = Lexical(test_file)
tokens = lexer.tokenize()

print(f"\nTotal tokens encontrados: {len(tokens)}")