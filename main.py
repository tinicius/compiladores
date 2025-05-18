import sys
from lib.lexical.lexical import Lexical
from lib.syntatic.systatic import Syntatic

def main():
    if len(sys.argv) < 2:
        raise ValueError("Please provide a filename as an argument.")

    filename = sys.argv[1]
    
    lexical = Lexical(filename)

    tokens = lexical.tokenize()
    
    for token in tokens:
        lexical.print_token(token)

    syntatic = Syntatic(tokens)
    syntatic.start()


if __name__ == "__main__":
    main()
