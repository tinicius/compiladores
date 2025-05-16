from lib.lexical.token import Token
from lib.lexical.token_type import TokenType


class Syntatic:
    def __init__(self, tokens: list[Token] = []):

        self.tokens: list[Token] = tokens

        self.current_token: Token = Token(
            TokenType.RESERVED_WORD_END, "None", 0, 0)

    def advance(self):
        """
        Move to the next token in the list.
        """
        if self.tokens:
            self.current_token = self.tokens.pop(0)

    def eat(self, token_type: TokenType):
        """
        Consume the current token if it matches the expected type.
        """
        if self.current_token is None:
            raise Exception("Unexpected end of input")

        if token_type == self.current_token.token_type:
            self.advance()

    def start(self):
        self.advance()

        self.procFunction()

    def procFunction(self):
        self.eat(TokenType.RESERVED_WORD_PROGRAM)
        self.eat(TokenType.VARIABLE)
        self.eat(TokenType.SEMICOLON)

        self.procDeclarations()

        self.eat(TokenType.RESERVED_WORD_BEGIN)

        self.procStmtList()

        self.eat(TokenType.RESERVED_WORD_END)
        self.eat(TokenType.DOT)

    def procDeclarations(self):
        self.eat(TokenType.RESERVED_WORD_VAR)

        self.procDeclaration()
        self.procRestoDeclaration()

    def procDeclaration(self):
        self.procListIdent()
        self.eat(TokenType.COLON)

        self.procType()

        self.eat(TokenType.SEMICOLON)

    def procListIdent(self):
        self.eat(TokenType.VARIABLE)
        self.procRestoListIdent()

    def procRestoListIdent(self):
        if self.current_token.token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            self.eat(TokenType.VARIABLE)
            self.procRestoListIdent()

    def procRestoDeclaration(self):
        if self.current_token.token_type == TokenType.VARIABLE:
            self.procDeclaration()
            self.procRestoDeclaration()

    def procType(self):
        if self.current_token.token_type == TokenType.RESERVED_WORD_INTEGER:
            self.eat(TokenType.RESERVED_WORD_INTEGER)
        elif self.current_token.token_type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
        elif self.current_token.token_type == TokenType.RESERVED_WORD_STRING:
            self.eat(TokenType.RESERVED_WORD_STRING)

    def procBloco(self):
        self.eat(TokenType.RESERVED_WORD_BEGIN)
        self.procStmtList()
        self.eat(TokenType.RESERVED_WORD_END)
        self.eat(TokenType.SEMICOLON)

    def procStmtList(self):
        if self.current_token.token_type in {TokenType.RESERVED_WORD_FOR, TokenType.RESERVED_WORD_READ, TokenType.RESERVED_WORD_WRITE, TokenType.RESERVED_WORD_READLN, TokenType.RESERVED_WORD_WRITELN, TokenType.RESERVED_WORD_WHILE, TokenType.VARIABLE, TokenType.RESERVED_WORD_IF, TokenType.RESERVED_WORD_BEGIN, TokenType.RESERVED_WORD_BREAK, TokenType.RESERVED_WORD_CONTINUE, TokenType.SEMICOLON}:
            self.procStmt()
            self.procStmtList()

    def procStmt(self):
        if self.current_token.token_type == TokenType.RESERVED_WORD_FOR:
            self.procForStmt()
        elif self.current_token.token_type in {TokenType.RESERVED_WORD_READ, TokenType.RESERVED_WORD_WRITE, TokenType.RESERVED_WORD_READLN, TokenType.RESERVED_WORD_WRITELN}:
            self.procIoStmt()
        elif self.current_token.token_type == TokenType.VARIABLE:
            self.procAtrib()
            self.eat(TokenType.SEMICOLON)
        elif self.current_token.token_type == TokenType.RESERVED_WORD_IF:
            self.procIfStmt()
        elif self.current_token.token_type == TokenType.RESERVED_WORD_BEGIN:
            self.procBloco()
        elif self.current_token.token_type == TokenType.RESERVED_WORD_BREAK:
            self.eat(TokenType.RESERVED_WORD_BREAK)
            self.eat(TokenType.SEMICOLON)
        elif self.current_token.token_type == TokenType.RESERVED_WORD_CONTINUE:
            self.eat(TokenType.RESERVED_WORD_CONTINUE)
            self.eat(TokenType.SEMICOLON)
        else:
            self.eat(TokenType.SEMICOLON)

    def procForStmt(self):
        self.eat(TokenType.RESERVED_WORD_FOR)
        self.procAtrib()
        self.eat(TokenType.RESERVED_WORD_TO)
        self.procEndFor()
        self.eat(TokenType.RESERVED_WORD_DO)
        self.procStmt()

    def procEndFor(self):
        if self.current_token.token_type == TokenType.VARIABLE:
            self.eat(TokenType.VARIABLE)
        if self.current_token.token_type == TokenType.DECIMAL:
            self.eat(TokenType.DECIMAL)
        if self.current_token.token_type == TokenType.OCTAL:
            self.eat(TokenType.OCTAL)
        else:
            self.eat(TokenType.HEXADECIMAL)

    def procIoStmt(self):
        if self.current_token.token_type == TokenType.RESERVED_WORD_READ:
            self.eat(TokenType.RESERVED_WORD_READ)
            self.eat(TokenType.OPEN_PARENTHESES)
            self.eat(TokenType.VARIABLE)
            self.eat(TokenType.CLOSE_PARENTHESES)
            self.eat(TokenType.SEMICOLON)
        elif self.current_token.token_type == TokenType.RESERVED_WORD_WRITE:
            self.eat(TokenType.RESERVED_WORD_WRITE)
            self.eat(TokenType.OPEN_PARENTHESES)
            self.procOutList()
            self.eat(TokenType.CLOSE_PARENTHESES)
            self.eat(TokenType.SEMICOLON)
        elif self.current_token.token_type == TokenType.RESERVED_WORD_READLN:
            self.eat(TokenType.RESERVED_WORD_READLN)
            self.eat(TokenType.OPEN_PARENTHESES)
            self.eat(TokenType.VARIABLE)
            self.eat(TokenType.CLOSE_PARENTHESES)
            self.eat(TokenType.SEMICOLON)
        else:
            self.eat(TokenType.RESERVED_WORD_WRITELN)
            self.eat(TokenType.OPEN_PARENTHESES)
            self.procOutList()
            self.eat(TokenType.CLOSE_PARENTHESES)
            self.eat(TokenType.SEMICOLON)

    def procOutList(self):
        self.procOut()
        self.procRestoOutList()

    def procRestoOutList(self):
        if self.current_token.token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            self.procOutList()

    def procOut(self):
        if self.current_token.token_type == TokenType.STRING:
            self.eat(TokenType.STRING)
        elif self.current_token.token_type == TokenType.VARIABLE:
            self.eat(TokenType.VARIABLE)
        elif self.current_token.token_type == TokenType.DECIMAL:
            self.eat(TokenType.DECIMAL)
        elif self.current_token.token_type == TokenType.OCTAL:
            self.eat(TokenType.OCTAL)
        elif self.current_token.token_type == TokenType.HEXADECIMAL:
            self.eat(TokenType.HEXADECIMAL)
        else:
            self.eat(TokenType.FLOAT)

    def procWhileStmt(self):
        self.eat(TokenType.RESERVED_WORD_WHILE)
        self.procExpr()
        self.eat(TokenType.RESERVED_WORD_DO)
        self.procStmt()

    def procIfStmt(self):
        self.eat(TokenType.RESERVED_WORD_IF)
        self.procExpr()
        self.eat(TokenType.RESERVED_WORD_THEN)
        self.procStmt()
        self.procElsePart()

    def procElsePart(self):
        if self.current_token.token_type == TokenType.RESERVED_WORD_ELSE:
            self.eat(TokenType.RESERVED_WORD_ELSE)
            self.procStmt()

    def procAtrib(self):
        self.eat(TokenType.VARIABLE)
        self.eat(TokenType.OPERATOR_ASSIGN)
        self.procExpr()

    def procExpr(self):
        self.procOr()

    def procOr(self):
        self.procAnd()
        self.procRestoOr()

    def procRestoOr(self):
        if self.current_token.token_type == TokenType.OPERATOR_OR:
            self.eat(TokenType.OPERATOR_OR)
            self.procAnd()
            self.procRestoOr()

    def procAnd(self):
        self.procNot()
        self.procRestoAnd()

    def procRestoAnd(self):
        if self.current_token.token_type == TokenType.OPERATOR_AND:
            self.eat(TokenType.OPERATOR_AND)
            self.procNot()
            self.procRestoAnd()

    def procNot(self):
        if self.current_token.token_type == TokenType.OPERATOR_NOT:
            self.eat(TokenType.OPERATOR_NOT)
            self.procNot()
        else:
            self.procRel()

    def procRel(self):
        self.procAdd()
        self.procRestoRel()

    def procRestoRel(self):
        if self.current_token.token_type == TokenType.OPERATOR_EQUAL:
            self.eat(TokenType.OPERATOR_EQUAL)
            self.procAdd()
        elif self.current_token.token_type == TokenType.OPERATOR_NOT_EQUAL:
            self.eat(TokenType.OPERATOR_NOT_EQUAL)
            self.procAdd()
        elif self.current_token.token_type == TokenType.OPERATOR_LESS:
            self.eat(TokenType.OPERATOR_LESS)
            self.procAdd()
        elif self.current_token.token_type == TokenType.OPERATOR_LESS_EQUAL:
            self.eat(TokenType.OPERATOR_LESS_EQUAL)
            self.procAdd()
        elif self.current_token.token_type == TokenType.OPERATOR_GREATER:
            self.eat(TokenType.OPERATOR_GREATER)
            self.procAdd()
        elif self.current_token.token_type == TokenType.OPERATOR_GREATER_EQUAL:
            self.eat(TokenType.OPERATOR_GREATER_EQUAL)
            self.procAdd()

    def procAdd(self):
        self.procMult()
        self.procRestoAdd()

    def procRestoAdd(self):
        if self.current_token.token_type == TokenType.OPERATOR_PLUS:
            self.eat(TokenType.OPERATOR_PLUS)
            self.procMult()
            self.procRestoAdd()
        elif self.current_token.token_type == TokenType.OPERATOR_MINUS:
            self.eat(TokenType.OPERATOR_MINUS)
            self.procMult()
            self.procRestoAdd()

    def procMult(self):
        self.procUno()
        self.procRestoMult()

    def procRestoMult(self):
        if self.current_token.token_type == TokenType.OPERATOR_MULTIPLY:
            self.eat(TokenType.OPERATOR_MULTIPLY)
            self.procUno()
            self.procRestoMult()
        elif self.current_token.token_type == TokenType.OPERATOR_DIVIDE:
            self.eat(TokenType.OPERATOR_DIVIDE)
            self.procUno()
            self.procRestoMult()
        elif self.current_token.token_type == TokenType.OPERATOR_MOD:
            self.eat(TokenType.OPERATOR_MOD)
            self.procUno()
            self.procRestoMult()
        elif self.current_token.token_type == TokenType.OPERATOR_INTEGER_DIVIDER:
            self.eat(TokenType.OPERATOR_INTEGER_DIVIDER)
            self.procUno()
            self.procRestoMult()

    def procUno(self):
        if self.current_token.token_type == TokenType.OPERATOR_PLUS:
            self.eat(TokenType.OPERATOR_PLUS)
            self.procUno()
        elif self.current_token.token_type == TokenType.OPERATOR_MINUS:
            self.eat(TokenType.OPERATOR_MINUS)
            self.procUno()
        else:
            self.procFactor()

    def procFactor(self):
        if self.current_token.token_type == TokenType.DECIMAL:
            self.eat(TokenType.DECIMAL)
        elif self.current_token.token_type == TokenType.OCTAL:
            self.eat(TokenType.OCTAL)
        elif self.current_token.token_type == TokenType.HEXADECIMAL:
            self.eat(TokenType.HEXADECIMAL)
        elif self.current_token.token_type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
        elif self.current_token.token_type == TokenType.VARIABLE:
            self.eat(TokenType.VARIABLE)
        elif self.current_token.token_type == TokenType.OPEN_PARENTHESES:
            self.eat(TokenType.OPEN_PARENTHESES)
            self.procExpr()
            self.eat(TokenType.CLOSE_PARENTHESES)
        else:
            self.eat(TokenType.STRING)
