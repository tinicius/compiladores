from lib.lexical.token_type import TokenType
from lib.lexical.token import Token
from lib.lexical.errors import StringError, InvalidNumberError
from lib.lexical.token_map import token_map


class Lexical:
    def __init__(self, filename: str):
        try:
            with open(filename, "r") as file_handle:
                self.input = list(file_handle)
        except FileNotFoundError:
            raise Exception(f"Error: The file {filename} does not exist.")

        self.line = 0
        self.column = 0

        self.idx = 0

        self.numbers_delimiters = {" ", "\t", "\n", "(", ")", "{", "}", ",", ";", ":", "+", "-", "*", "/", "=", "<", ">", '"', "'", "\\"}

        self.hexadecimal_characters = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"}

        self.octal_characters = {"0", "1", "2", "3", "4", "5", "6", "7"}

        self.brace_delimiters = {"\n", " ", "\t"}

    def get_char(self) -> str:
        try:

            if self.line >= len(self.input):
                return ""

            if self.idx >= len(self.input[self.line]):
                return ""

            c = self.input[self.line][self.idx]
            self.idx += 1

            return c
        except:
            raise Exception("Error: Unable to read character from file.")

    def nextToken(self) -> Token:

        state = 0
        start_column = self.column
        token_buffer = ""
        c = ""

        while state != 2 and state != 14:
            c = self.get_char()
            self.column += 1

            if c == "":
                if state == 1:
                    state = 2
                    break

                if state in {5, 7, 9, 10}:
                    break

                if state == 6:
                    raise StringError(f"Invalid string at: {self.line}, {self.column}")

                if state == 11:
                    if token_buffer[len(token_buffer) - 1] == ".":
                        token_buffer += "0"

                    break

                return Token(TokenType.EOF, "", self.line, 0)

            match state:
                case 0:
                    if c.isalpha():
                        token_buffer += c
                        state = 1
                    elif c == "0":
                        token_buffer += c
                        state = 5
                    elif c.isdigit():
                        token_buffer += c
                        state = 10
                    elif c == '"':
                        token_buffer += c
                        state = 6
                    elif c == '+':
                        token_buffer += c
                        return Token(TokenType.OPERATOR_PLUS, token_buffer, self.line, start_column)
                    elif c == '-':
                        token_buffer += c
                        return Token(TokenType.OPERATOR_MINUS, token_buffer, self.line, start_column)
                    elif c == '*':
                        token_buffer += c
                        return Token(TokenType.OPERATOR_MULTIPLY, token_buffer, self.line, start_column)
                    elif c == '/':
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char == "/":
                            token_buffer += next_char
                            self.line += 1
                            self.idx = 0
                            self.column = 0
                            break
                        else:
                            if next_char != "":
                                self.idx -= 1
                            return Token(TokenType.OPERATOR_DIVIDE, token_buffer, self.line, start_column)
                    elif c == "=":
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char == "=":
                            token_buffer += next_char
                            self.column += 1
                            return Token(TokenType.OPERATOR_EQUAL, token_buffer, self.line, start_column)
                        else:
                            if next_char != "":
                                self.idx -= 1
                            return Token(TokenType.OPERATOR_EQUAL, token_buffer, self.line, start_column)
                    elif c == "<":
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char == ">":
                            token_buffer += next_char
                            self.column += 1
                            return Token(TokenType.OPERATOR_NOT_EQUAL, token_buffer, self.line, start_column)
                        elif next_char == "=":
                            token_buffer += next_char
                            self.column += 1
                            return Token(TokenType.OPERATOR_LESS_EQUAL, token_buffer, self.line, start_column)
                        else:
                            if next_char != "":
                                self.idx -= 1
                            return Token(TokenType.OPERATOR_LESS, token_buffer, self.line, start_column)
                    elif c == ">":
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char == "=":
                            token_buffer += next_char
                            self.column += 1
                            return Token(TokenType.OPERATOR_GREATER_EQUAL, token_buffer, self.line, start_column)
                        else:
                            if next_char != "":
                                self.idx -= 1
                            return Token(TokenType.OPERATOR_GREATER, token_buffer, self.line, start_column)
                    elif c == ":":
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char == "=":
                            token_buffer += next_char
                            self.column += 1
                            return Token(TokenType.OPERATOR_ASSIGN, token_buffer, self.line, start_column)
                        else:
                            if next_char != "":
                                self.idx -= 1
                            return Token(TokenType.COLON, token_buffer, self.line, start_column)
                    elif c == ";":
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char != "":
                            self.idx -= 1
                        return Token(TokenType.SEMICOLON, token_buffer, self.line, start_column)
                    elif c == ",":
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char != "":
                            self.idx -= 1
                        return Token(TokenType.COMMA, token_buffer, self.line, start_column)
                    elif c == ".":
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char != "":
                            self.idx -= 1
                        return Token(TokenType.DOT, token_buffer, self.line, start_column)
                    elif c == "(":
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char != "":
                            self.idx -= 1
                        return Token(TokenType.OPEN_PARENTHESES, token_buffer, self.line, start_column)
                    elif c == ")":
                        token_buffer += c
                        next_char = self.get_char()
                        if next_char != "":
                            self.idx -= 1
                        return Token(TokenType.CLOSE_PARENTHESES, token_buffer, self.line, start_column)
                    elif c == "{":
                        start_column = self.column - 1
                        while True:
                            next_char = self.get_char()
                            if next_char == "":
                                raise Exception(f"Error: Unclosed block comment starting at line {self.line} column {self.column}.")
                            if next_char == "}":
                                break
                            if next_char == "\n":
                                self.line += 1
                                self.idx = 0
                                self.column = 0
                            else:
                                self.column += 1
                        break
                    elif c == "}":
                        raise Exception(f"Error: Unmatched closing brace at line {self.line} column {self.column}")
                    elif c in self.brace_delimiters:
                        break
                    else:
                        raise Exception(f"Error: Invalid character at line {self.line} column {start_column}.")
                case 1:
                    if c.isalpha() or c.isdigit():
                        token_buffer += c
                        state = 1
                    else:
                        self.idx -= 1
                        self.column -= 1
                        state = 2
                case 5:
                    if c in self.octal_characters:
                        token_buffer += c
                        state = 7
                    elif c == "x":
                        token_buffer += c
                        state = 8
                    elif c == ".":
                        token_buffer += c
                        state = 11
                    elif c in self.numbers_delimiters:
                        self.idx -= 1
                        self.column -= 1
                        break
                    else:
                        raise InvalidNumberError(f"Error: Invalid digit at line {self.line} column {self.column}.")
                case 6:
                    if c == "\\":
                        state = 13
                    elif c == '"':
                        token_buffer += c
                        state = 14
                    elif c == "\n":
                        raise StringError(f"Invalid string at: {self.line}, {self.column}")
                    else:
                        token_buffer += c
                        state = 6
                case 7:
                    if c == ".":
                        token_buffer += c
                        state = 11
                    elif c in self.octal_characters:
                        token_buffer += c
                        state = 7
                    elif c in self.numbers_delimiters:
                        self.idx -= 1
                        self.column -= 1
                        break
                    else:
                        raise InvalidNumberError(f"Error: Invalid octal digit at line {self.line} column {self.column}.")
                case 8:
                    if c in self.hexadecimal_characters:
                        token_buffer += c
                        state = 9
                    elif c in self.numbers_delimiters:
                        raise InvalidNumberError(f"Error: Incomplete hexadecimal number at line {self.line} column {start_column}.")
                    else:
                        raise InvalidNumberError(f"Error: Invalid hexadecimal digit at line {self.line} column {self.column}.")
                case 9:
                    if c in self.hexadecimal_characters:
                        token_buffer += c
                        state = 9
                    elif c in self.numbers_delimiters:
                        self.idx -= 1
                        self.column -= 1
                        break
                    else:
                        raise InvalidNumberError(f"Error: Invalid hexadecimal digit at line {self.line} column {self.column}.")
                case 10:
                    if c.isdigit():
                        token_buffer += c
                        state = 10
                    elif c == ".":
                        token_buffer += c
                        state = 11
                    elif c in self.numbers_delimiters:
                        self.idx -= 1
                        self.column -= 1
                        break
                    else:
                        raise InvalidNumberError(f"Error: Invalid digit at line {self.line} column {self.column}.")
                case 11:
                    if c.isdigit():
                        token_buffer += c
                        state = 11
                    elif c in self.numbers_delimiters:
                        if token_buffer[len(token_buffer) - 1] == ".":
                            token_buffer += "0"

                        self.idx -= 1
                        self.column -= 1
                        break
                    else:
                        raise InvalidNumberError(f"Error: Invalid float number at line {self.line} column {self.column}.")
                case 13:
                    if c == "n":
                        token_buffer += "\n"
                        state = 6
                    elif c == "r":
                        token_buffer += "\r"
                        state = 6
                    elif c == "t":
                        token_buffer += "\t"
                        state = 6
                    elif c == "0":
                        token_buffer += "\0"
                        state = 6
                    elif c == '"':
                        token_buffer += c
                        state = 14
                    else:
                        token_buffer += c
                        state = 6

        token = None

        if state == 2:
            if token_map.get(token_buffer) is not None:
                token = Token(token_map[token_buffer], token_buffer, self.line, start_column)
            else:
                token = Token(TokenType.VARIABLE, token_buffer, self.line, start_column)
        elif state == 5:  # Adicione este caso para o número 0
            token = Token(TokenType.OCTAL, token_buffer, self.line, start_column)
        elif state == 7:
            token = Token(TokenType.OCTAL, token_buffer, self.line, start_column)
        elif state == 9:
            token = Token(TokenType.HEXADECIMAL, token_buffer, self.line, start_column)
        elif state == 10:
            token = Token(TokenType.DECIMAL, token_buffer, self.line, start_column)
        elif state == 11:
            token = Token(TokenType.FLOAT, token_buffer, self.line, start_column)

        if state == 14:
            token = Token(TokenType.STRING, token_buffer, self.line, start_column)

        if c == "\n":
            self.line += 1
            self.idx = 0
            self.column = 0

        return token

    def print_token(self, token: Token):
        print(f"({token.token_type}, {token.lexeme}, {token.line}, {token.column})")

    def tokenize(self) -> list[Token]:
        tokens = []

        while True:
            token = self.nextToken()

            if token is None:
                continue

            if token.token_type == TokenType.EOF:
                break

            tokens.append(token)

        return tokens
