from lib.lexical.token import Token
from lib.lexical.token_type import TokenType
from lib.syntatic.command import Command


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

    def eat(self, token_type: TokenType, next_token: bool = True):
        """
        Consume the current token if it matches the expected type.
        """
        if self.current_token is None:
            raise Exception("Unexpected end of input")

        if token_type == self.current_token.token_type:
            if next_token:
                self.advance()
        else:
            raise Exception(
                f"Expected token type {token_type}, but got {self.current_token.token_type} at line {self.current_token.line}, column {self.current_token.column}")

    def start(self):
        self.advance()

        return self.procFunction()

    def procFunction(self):
        """
            <function*> -> 'program' 'IDENT' ';' <declarations> 'begin' <stmtList> 'end' '.' ;
        """

        aux = []

        self.eat(TokenType.RESERVED_WORD_PROGRAM)
        self.eat(TokenType.VARIABLE)
        self.eat(TokenType.SEMICOLON)

        self.procDeclarations()

        self.eat(TokenType.RESERVED_WORD_BEGIN)

        aux.extend(self.procStmtList())

        self.eat(TokenType.RESERVED_WORD_END)
        self.eat(TokenType.DOT, next_token=False)

        if len(self.tokens) > 0:
            raise Exception(
                f"Unexpected tokens after end of program: {self.tokens}")

        return aux

    def procDeclarations(self):
        """
            <declarations> -> var <declaration> <restoDeclaration> ;
        """

        self.eat(TokenType.RESERVED_WORD_VAR)

        self.procDeclaration()
        self.procRestoDeclaration()

    def procDeclaration(self):
        """
            <declaration> -> <listaIdent> ':' <type> ';' ;
        """

        self.procListIdent()
        self.eat(TokenType.COLON)

        self.procType()

        self.eat(TokenType.SEMICOLON)

    def procListIdent(self):
        """
            <listaIdent> -> 'IDENT' <restoIdentList> ;
        """

        self.eat(TokenType.VARIABLE)
        self.procRestoListIdent()

    def procRestoListIdent(self):
        """
            <restoIdentList> -> ',' 'IDENT' <restoIdentList> | & ;
        """

        if self.current_token.token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            self.eat(TokenType.VARIABLE)
            self.procRestoListIdent()
        else:
            pass

    def procRestoDeclaration(self):
        """
            <restoDeclaration> -> <declaration> <restoDeclaration> | & ;
        """

        if self.current_token.token_type == TokenType.VARIABLE:
            self.procDeclaration()
            self.procRestoDeclaration()
        else:
            pass

    def procType(self):
        """
            <type> -> 'integer' | 'real' | 'string' ;
        """

        if self.current_token.token_type == TokenType.RESERVED_WORD_INTEGER:
            self.eat(TokenType.RESERVED_WORD_INTEGER)
        elif self.current_token.token_type == TokenType.RESERVED_WORD_REAL:
            self.eat(TokenType.RESERVED_WORD_REAL)
        else:
            self.eat(TokenType.RESERVED_WORD_STRING)

    def procBloco(self):
        """
            <bloco> -> 'begin' <stmtList> 'end' ';' ;
        """

        self.eat(TokenType.RESERVED_WORD_BEGIN)

        self.procStmtList()

        self.eat(TokenType.RESERVED_WORD_END)
        self.eat(TokenType.SEMICOLON)

    def procStmtList(self):
        """
            <stmtList> -> <stmt> <stmtList> | & ;
        """

        stmt = {
            # forStmt
            TokenType.RESERVED_WORD_FOR,

            # ioStmt
            TokenType.RESERVED_WORD_READ,
            TokenType.RESERVED_WORD_WRITE,
            TokenType.RESERVED_WORD_READLN,
            TokenType.RESERVED_WORD_WRITELN,

            # whileStmt
            TokenType.RESERVED_WORD_WHILE,

            # atrib
            TokenType.VARIABLE,

            # ifStmt
            TokenType.RESERVED_WORD_IF,

            # bloco
            TokenType.RESERVED_WORD_BEGIN,

            TokenType.RESERVED_WORD_BREAK,
            TokenType.RESERVED_WORD_CONTINUE,
            TokenType.SEMICOLON
        }

        if self.current_token.token_type in stmt:
            aux = []

            aux.extend(self.procStmt())
            aux.extend(self.procStmtList())

            return aux
        else:
            return []

    def procStmt(self):
        """
            <stmt> -> <forStmt> 
                    | <ioStmt>
                    | <whileStmt>
                    | <atrib> ';'
                    | <ifStmt> 
                    | <bloco> 
                    | 'break'';'
                    | 'continue'';'
                    | ';' ;
        """

        io = {
            TokenType.RESERVED_WORD_READ,
            TokenType.RESERVED_WORD_WRITE,
            TokenType.RESERVED_WORD_READLN,
            TokenType.RESERVED_WORD_WRITELN
        }

        if self.current_token.token_type == TokenType.RESERVED_WORD_FOR:
            self.procForStmt()
        elif self.current_token.token_type in io:
            return self.procIoStmt()
        elif self.current_token.token_type == TokenType.RESERVED_WORD_WHILE:
            self.procWhileStmt()
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

        return []

    def procForStmt(self):
        """
            <forStmt> -> 'for' <atrib> 'to' <endFor> 'do' <stmt> ;
        """

        self.eat(TokenType.RESERVED_WORD_FOR)

        self.procAtrib()

        self.eat(TokenType.RESERVED_WORD_TO)

        self.procEndFor()

        self.eat(TokenType.RESERVED_WORD_DO)

        self.procStmt()

    def procEndFor(self):
        """
            <endFor> -> 'IDENT' | 'NUMint' ;
        """

        if self.current_token.token_type == TokenType.VARIABLE:
            self.eat(TokenType.VARIABLE)
        if self.current_token.token_type == TokenType.DECIMAL:
            self.eat(TokenType.DECIMAL)
        if self.current_token.token_type == TokenType.OCTAL:
            self.eat(TokenType.OCTAL)
        else:
            self.eat(TokenType.HEXADECIMAL)

    def procIoStmt(self):
        """
            <ioStmt> ->   'read' '(' 'IDENT' ')' ';' 
                        | 'write' '(' <outList> ')' ';' ;
                        | 'readln' '(' 'IDENT' ')' ';'
                        | 'writeln' '(' <outList> ')' ';' ;
        """

        aux = []

        if self.current_token.token_type == TokenType.RESERVED_WORD_READ:
            self.eat(TokenType.RESERVED_WORD_READ)
            self.eat(TokenType.OPEN_PARENTHESES)
            self.eat(TokenType.VARIABLE)
            self.eat(TokenType.CLOSE_PARENTHESES)
            self.eat(TokenType.SEMICOLON)
        elif self.current_token.token_type == TokenType.RESERVED_WORD_WRITE:
            self.eat(TokenType.RESERVED_WORD_WRITE)
            self.eat(TokenType.OPEN_PARENTHESES)

            aux.extend(self.procOutList())

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

            aux.extend(self.procOutList())
            aux.append((Command.CALL, "WRITE", "\n"))

            self.eat(TokenType.CLOSE_PARENTHESES)
            self.eat(TokenType.SEMICOLON)

        return aux

    def procOutList(self):
        """
            <outList> -> <out> <restoOutList> ;
        """

        aux = []

        aux.extend(self.procOut())
        aux.extend(self.procRestoOutList())

        return aux

    def procRestoOutList(self):
        """
            <restoOutList> -> ',' <outList> | & ;
        """

        if self.current_token.token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            return self.procOutList()
        else:
            return []

    def procOut(self):
        """
            <out> -> 'STR' | 'IDENT' | 'NUMint' | 'NUMfloat' ;
        """

        command = []

        if self.current_token.token_type == TokenType.STRING:
            command.append((Command.CALL, "WRITE", self.current_token.lexeme))
            self.eat(TokenType.STRING)
        elif self.current_token.token_type == TokenType.VARIABLE:
            command.append((Command.CALL, "WRITE", None,
                           self.current_token.lexeme))
            self.eat(TokenType.VARIABLE)
        elif self.current_token.token_type == TokenType.DECIMAL:
            self.eat(TokenType.DECIMAL)
            return []
        elif self.current_token.token_type == TokenType.OCTAL:
            self.eat(TokenType.OCTAL)
            return []
        elif self.current_token.token_type == TokenType.HEXADECIMAL:
            self.eat(TokenType.HEXADECIMAL)
            return []
        else:
            self.eat(TokenType.FLOAT)
            return []

        return command

    def procWhileStmt(self):
        """
            <whileStmt> -> 'while' <expr> 'do' <stmt> ;
        """

        self.eat(TokenType.RESERVED_WORD_WHILE)

        self.procExpr()

        self.eat(TokenType.RESERVED_WORD_DO)

        self.procStmt()

    def procIfStmt(self):
        """
            <ifStmt> -> 'if' <expr> 'then' <stmt> <elsePart> ;
        """

        self.eat(TokenType.RESERVED_WORD_IF)

        self.procExpr()

        self.eat(TokenType.RESERVED_WORD_THEN)

        self.procStmt()
        self.procElsePart()

    def procElsePart(self):
        """
            <elsePart> -> 'else' <stmt> | & ;
        """

        if self.current_token.token_type == TokenType.RESERVED_WORD_ELSE:
            self.eat(TokenType.RESERVED_WORD_ELSE)
            self.procStmt()
        else:
            pass

    def procAtrib(self):
        """
            <atrib> -> 'IDENT' ':=' <expr> ;
        """

        self.eat(TokenType.VARIABLE)
        self.eat(TokenType.OPERATOR_ASSIGN)

        self.procExpr()

    def procExpr(self):
        """
            <expr> -> <or> ;
        """

        self.procOr()

    def procOr(self):
        """
            <or> -> <and> <restoOr> ;
        """

        self.procAnd()
        self.procRestoOr()

    def procRestoOr(self):
        """
            <restoOr> -> 'or' <and> <restoOr> | & ;
        """

        if self.current_token.token_type == TokenType.OPERATOR_OR:
            self.eat(TokenType.OPERATOR_OR)
            self.procAnd()
            self.procRestoOr()
        else:
            pass

    def procAnd(self):
        """
            <and> -> <not> <restoAnd> ;
        """

        self.procNot()
        self.procRestoAnd()

    def procRestoAnd(self):
        """
            <restoAnd> -> 'and' <not> <restoAnd> | & ;
        """

        if self.current_token.token_type == TokenType.OPERATOR_AND:
            self.eat(TokenType.OPERATOR_AND)
            self.procNot()
            self.procRestoAnd()
        else:
            pass

    def procNot(self):
        """
            <not> -> 'not' <not> | <rel> ;
        """

        if self.current_token.token_type == TokenType.OPERATOR_NOT:
            self.eat(TokenType.OPERATOR_NOT)
            self.procNot()
        else:
            self.procRel()

    def procRel(self):
        """
            <rel> -> <add> <restoRel> ;
        """

        self.procAdd()
        self.procRestoRel()

    def procRestoRel(self):
        """
            <restoRel> -> '==' <add> 
                        | '<>' <add>
                        | '<' <add> 
                        | '<=' <add> 
                        | '>' <add> 
                        | '>=' <add> 
                        | & ;
        """

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
        else:
            pass

    def procAdd(self):
        """
            <add> -> <mult> <restoAdd> ;
        """

        self.procMult()
        self.procRestoAdd()

    def procRestoAdd(self):
        """
            <restoAdd> -> '+' <mult> <restoAdd> 
                        | '-' <mult> <restoAdd> 
                        | & 
        """

        if self.current_token.token_type == TokenType.OPERATOR_PLUS:
            self.eat(TokenType.OPERATOR_PLUS)
            self.procMult()
            self.procRestoAdd()
        elif self.current_token.token_type == TokenType.OPERATOR_MINUS:
            self.eat(TokenType.OPERATOR_MINUS)
            self.procMult()
            self.procRestoAdd()
        else:
            pass

    def procMult(self):
        """
            <mult> -> <uno> <restoMult> ;
        """

        self.procUno()
        self.procRestoMult()

    def procRestoMult(self):
        """
            <restoMult> -> '*' <uno> <restoMult>
                        |  '/' <uno> <restoMult> 
                        |  'mod' <uno> <restoMult>
                        |  'div' <uno> <restoMult> 
                        |  & ;
        """

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
        else:
            pass

    def procUno(self):
        """
            <uno> ->  '+' <uno> 
                    | '-' <uno> 
                    | <fator> ;
        """

        if self.current_token.token_type == TokenType.OPERATOR_PLUS:
            self.eat(TokenType.OPERATOR_PLUS)
            self.procUno()
        elif self.current_token.token_type == TokenType.OPERATOR_MINUS:
            self.eat(TokenType.OPERATOR_MINUS)
            self.procUno()
        else:
            self.procFactor()

    def procFactor(self):
        """
            <fator> -> 'NUMint' 
                    |  'NUMfloat' 
                    |  'IDENT'  
                    |  '(' <expr> ')' 
                    |  'STR' ;
        """

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
