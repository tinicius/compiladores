import sys
from lexical.lexical import Lexical

def main():
    if len(sys.argv) < 2:
        raise ValueError("Please provide a filename as an argument.")

    filename = sys.argv[1]
    
    lexical = Lexical(filename)
    
    for token in lexical.tokenize():
        lexical.print_token(token)

if __name__ == "__main__":
    main()
