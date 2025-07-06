import sys
from lib.lexical.lexical import Lexical
from lib.syntatic.systatic import Syntatic
from lib.interpreter.interpreter import Interpreter
from lib.semantic.semantic import SemanticAnalyzer

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

    semantic = SemanticAnalyzer()
    if semantic.analyze(instructions):
        print("\n✅ Análise Semântica: OK")
        semantic.print_symbol_table()
    else:
        print("\n Análise Semântica: ERRO")
        
    print("\nExecutando programa:")
    interpreter = Interpreter(instructions)
    interpreter.run()

if __name__ == "__main__":
    main()
