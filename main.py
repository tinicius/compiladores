import sys
from lib.lexical.lexical import Lexical
from lib.syntatic.systatic import Syntatic
from lib.interpreter.interpreter import Interpreter


def main():
    if len(sys.argv) < 2:
        raise ValueError("Please provide a filename as an argument.")

    filename = sys.argv[1]

    lexical = Lexical(filename)

    tokens = lexical.tokenize()

    for token in tokens:
        lexical.print_token(token)

    syntatic = Syntatic(tokens)
    instructions = syntatic.start()

    print("\n")

    for instruction in instructions:
        print(instruction)

    print("\nExecutando programa:")
    interpreter = Interpreter(instructions)
    interpreter.run()

if __name__ == "__main__":
    main()
