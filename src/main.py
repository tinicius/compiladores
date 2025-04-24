from enum import Enum, auto

class TokenType(Enum):
    VARIABLE = auto()
    RESERVED_WORD_PROGRAM = auto()
    RESERVED_WORD_BEGIN = auto()
    RESERVED_WORD_END = auto()
    RESERVED_WORD_VAR = auto()
    RESERVED_WORD_INTEGER = auto()
    RESERVED_WORD_REAL = auto()
    RESERVED_WORD_STRING = auto()
    RESERVED_WORD_FOR = auto()
    RESERVED_WORD_TO = auto()
    RESERVED_WORD_WHILE = auto()
    RESERVED_WORD_DO = auto()
    RESERVED_WORD_BREAK = auto()
    RESERVED_WORD_CONTINUE = auto()
    RESERVED_WORD_IF = auto()
    RESERVED_WORD_ELSE = auto()
    RESERVED_WORD_THEN = auto()
    RESERVED_WORD_WRITE = auto()
    RESERVED_WORD_WRITELN = auto()
    RESERVED_WORD_READ = auto()
    RESERVED_WORD_READLN = auto()
    STRING = auto()
    OPEN_PARENTHESES = auto()
    CLOSE_PARENTHESES = auto()
    SEMICOLON = auto()
    DOT = auto()
    EOF = auto()
    
class StringError(Exception):
    pass

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

token_map: dict[str, TokenType] = {
    "program": TokenType.RESERVED_WORD_PROGRAM,
    "var": TokenType.RESERVED_WORD_VAR,
    "integer": TokenType.RESERVED_WORD_INTEGER,
    "real": TokenType.RESERVED_WORD_REAL,
    "string": TokenType.RESERVED_WORD_STRING,
    "begin": TokenType.RESERVED_WORD_BEGIN,
    "end": TokenType.RESERVED_WORD_END,
    "for": TokenType.RESERVED_WORD_FOR,
    "to": TokenType.RESERVED_WORD_TO,
    "while": TokenType.RESERVED_WORD_WHILE,
    "do": TokenType.RESERVED_WORD_DO,
    "break": TokenType.RESERVED_WORD_BREAK,
    "continue": TokenType.RESERVED_WORD_CONTINUE,
    "if": TokenType.RESERVED_WORD_IF,
    "else": TokenType.RESERVED_WORD_ELSE,
    "then": TokenType.RESERVED_WORD_THEN,
    "write": TokenType.RESERVED_WORD_WRITE,
    "writeln": TokenType.RESERVED_WORD_WRITELN,
    "read": TokenType.RESERVED_WORD_READ,
    "readln": TokenType.RESERVED_WORD_READLN,
}

class Lexical:
    def __init__(self, filename: str):
        try:
            with open(filename, 'r') as file_handle:
                self.input = list(file_handle)
        except FileNotFoundError:
            raise Exception(f"Error: The file {filename} does not exist.")

        self.line = 0
        self.column = 0

        self.idx = 0
    
    def get_char(self) -> str:
        try:

            if self.line >= len(self.input):
                return ''
        
            if self.idx >= len(self.input[self.line]):
                return ''

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

            if c == '':

                if state == 1:
                    state = 2
                    break
                
                if state == 6:
                    raise StringError(f"Invalid string at: {self.line}, {self.column}")
                
                return Token(TokenType.EOF, "", self.line, 0)
        
            match state:
                case 0:
                    if c.isalpha():
                        token_buffer += c
                        state = 1
                    elif c == '"':
                        token_buffer += c
                        state = 6
                    else:
                        break

                case 1:
                    if c.isalpha() or c.isdigit():
                        token_buffer += c
                        state = 1
                    else:
                        state = 2

                case 6:
                    if c == "\\":
                        state = 13
                    elif c == '"':
                        token_buffer += c
                        state = 14
                    elif c == '\n':
                        raise StringError(f"Invalid string at: {self.line}, {self.column}")
                    else:
                        token_buffer += c
                        state = 6

                case 13:
                    if c == 'n':
                        token_buffer += "\n"
                        state = 6
                    elif c == 'r':
                        token_buffer += '\r'
                        state = 6
                    elif c == 't':
                        token_buffer += '\t'
                        state = 6
                    elif c == '0':
                        token_buffer += '\0'
                        state = 6
                    elif c == '"':
                        token_buffer += c
                        state = 14
                    else:
                        token_buffer += c
                        state = 6
                    
                        
        token = None

        if state == 2:
            if (token_map.get(token_buffer) is not None):
                token = Token(token_map[token_buffer], token_buffer, self.line, start_column)
            else:
                token = Token(TokenType.VARIABLE, token_buffer, self.line, start_column)
        
        if state == 14:
            token = Token(TokenType.STRING, token_buffer, self.line, start_column)

        if c == '\n':
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

        for token in tokens:
            self.print_token(token)

        return tokens