from lib.lexical.token import Token
from lib.lexical.token_type import TokenType
from lib.syntatic.command import Command


class Syntatic:
    def __init__(self, tokens: list[Token] = []):
        self.tokens: list[Token] = tokens
        self.current_token: Token = Token(TokenType.RESERVED_WORD_END, "None", 0, 0)
        self.temp_counter = 0  
        self.label_counter = 0
        self.loop_stack = []

        self.symbol_table = {}    
        self.semantic_errors = [] 
    
    def generate_temp_var(self):
        """Gera uma variável temporária única"""
        self.temp_counter += 1
        return f"temp_{self.temp_counter}"

    def generate_label(self):
        """Gera um label único"""  
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def add_variable(self, var_name, var_type):
        """Adiciona variável na tabela de símbolos"""
        if var_name in self.symbol_table:
            self.semantic_errors.append(f"Variable '{var_name}' already declared")
        else:
            self.symbol_table[var_name] = var_type

    def check_variable_declared(self, var_name):
        """Verifica se variável foi declarada"""
        if var_name not in self.symbol_table:
            self.semantic_errors.append(f"Variable '{var_name}' not declared")
            return False
        return True

    def get_variable_type(self, var_name):
        """Retorna tipo da variável"""
        return self.symbol_table.get(var_name, 'unknown')
    
    def get_expression_type(self, expression):
        """Determina o tipo de uma expressão"""
        if isinstance(expression, str):
            expression = expression.strip()
            
            if expression.startswith("'") and expression.endswith("'"):
                value = expression[1:-1]
                if '.' in value:
                    return 'real'
                else:
                    return 'integer'
            elif expression.startswith('"') and expression.endswith('"'):
                return 'string'
            elif expression.startswith('temp_'):
                return 'integer'  
            else:
                var_type = self.get_variable_type(expression)
                if var_type == 'unknown':
                    self.semantic_errors.append(f"Variable '{expression}' not declared")
                return var_type
        return 'unknown'

    def types_compatible(self, type1, type2):
        """Verifica se dois tipos são compatíveis"""
        if type1 == 'unknown' or type2 == 'unknown':
            return False

        if type1 == type2:
            return True

        if type1 == 'real' and type2 == 'integer':
            return True
        return False

    def print_symbol_table(self):
        """Imprime a tabela de símbolos para debug"""
        print("\n=== SYMBOL TABLE ===")
        for name, var_type in self.symbol_table.items():
            print(f"{name}: {var_type}")

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
        """<function*> -> 'program' 'IDENT' ';' <declarations> 'begin' <stmtList> 'end' '.' ;"""
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
            raise Exception(f"Unexpected tokens after end of program: {self.tokens}")

        return aux

    def procDeclarations(self):
        """<declarations> -> var <declaration> <restoDeclaration> ;"""
        self.eat(TokenType.RESERVED_WORD_VAR)

        self.procDeclaration()      
        self.procRestoDeclaration() 

        if self.semantic_errors:
            raise Exception(f"Semantic errors: {self.semantic_errors}") 

    def procDeclaration(self):
        """<declaration> -> <listaIdent> ':' <type> ';' ;"""
        var_list = self.procListIdent()
        self.eat(TokenType.COLON)
        var_type = self.procType()
        self.eat(TokenType.SEMICOLON)

        for var_name in var_list:
            self.add_variable(var_name, var_type)

        return []

    def procListIdent(self):
        """<listaIdent> -> 'IDENT' <restoIdentList> ;"""
        var_list = []
        var_list.append(self.current_token.lexeme) 
        self.eat(TokenType.VARIABLE)

        more_vars = self.procRestoListIdent()
        var_list.extend(more_vars)  

        return var_list

    def procRestoListIdent(self):
        """<restoIdentList> -> ',' 'IDENT' <restoIdentList> | & ;"""
        if self.current_token.token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_name = self.current_token.lexeme  
            self.eat(TokenType.VARIABLE)
            more_vars = self.procRestoListIdent()
            return [var_name] + more_vars 
        else:
            return []

    def procRestoDeclaration(self):
        """<restoDeclaration> -> <declaration> <restoDeclaration> | & ;"""
        if self.current_token.token_type == TokenType.VARIABLE:
            self.procDeclaration()     
            self.procRestoDeclaration()         
        else:
            return []

    def procType(self):
        """<type> -> 'integer' | 'real' | 'string' ;"""
        if self.current_token.token_type == TokenType.RESERVED_WORD_INTEGER:
            self.eat(TokenType.RESERVED_WORD_INTEGER)
            return 'integer'  
        elif self.current_token.token_type == TokenType.RESERVED_WORD_REAL:
            self.eat(TokenType.RESERVED_WORD_REAL)
            return 'real'     
        else:
            self.eat(TokenType.RESERVED_WORD_STRING)
            return 'string'

    def procBloco(self):
        """<bloco> -> 'begin' <stmtList> 'end' ';' ;"""
        self.eat(TokenType.RESERVED_WORD_BEGIN)
        commands = self.procStmtList()
        self.eat(TokenType.RESERVED_WORD_END)
     
        if self.current_token.token_type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return commands
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
            TokenType.RESERVED_WORD_ELSE,
            

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
            return self.procForStmt()
        elif self.current_token.token_type in io:
            return self.procIoStmt()
        elif self.current_token.token_type == TokenType.RESERVED_WORD_WHILE:
            return self.procWhileStmt()
        elif self.current_token.token_type == TokenType.VARIABLE:
            cmds = self.procAtrib()
            self.eat(TokenType.SEMICOLON)
            return cmds
        elif self.current_token.token_type == TokenType.RESERVED_WORD_IF:
            return self.procIfStmt()
        elif self.current_token.token_type == TokenType.RESERVED_WORD_ELSE:
            return self.procElsePart()
        elif self.current_token.token_type == TokenType.RESERVED_WORD_BEGIN:
            return self.procBloco() 
        elif self.current_token.token_type == TokenType.RESERVED_WORD_BREAK:
            self.eat(TokenType.RESERVED_WORD_BREAK)
            self.eat(TokenType.SEMICOLON)

            if not self.loop_stack:
                raise Exception("BREAK outside of loop")

            current_loop = self.loop_stack[-1]
            return [('JUMP', current_loop['end'], None, None)]
        elif self.current_token.token_type == TokenType.RESERVED_WORD_CONTINUE:
            self.eat(TokenType.RESERVED_WORD_CONTINUE)
            self.eat(TokenType.SEMICOLON)

            if not self.loop_stack:
                raise Exception("CONTINUE outside of loop")

            current_loop = self.loop_stack[-1]
            return [('JUMP', current_loop['start'], None, None)]
        else:
            self.eat(TokenType.SEMICOLON)

        return []

    def procForStmt(self):
        """<forStmt> -> 'for' <atrib> 'to' <endFor> 'do' <stmt> ;"""
        self.eat(TokenType.RESERVED_WORD_FOR)

        init_cmds = self.procAtrib()
        var_name = init_cmds[-1][1] 

        self.eat(TokenType.RESERVED_WORD_TO)

        end_cmds, end_value = self.procEndFor()

        for_counter = self.generate_label()
        loop_start = f'FOR_START_{for_counter}'
        loop_end = f'FOR_END_{for_counter}'
        
        self.loop_stack.append({
            'start': loop_start,
            'end': loop_end,
            'type': 'FOR'
        })

        self.eat(TokenType.RESERVED_WORD_DO)

        body_cmds = self.procStmt()
        commands = []

        commands.extend(init_cmds)

        commands.append(('LABEL', loop_start, None, None))

        temp_var = self.generate_temp_var()
        commands.append(('LEQ', temp_var, var_name, end_value))
        commands.append(('IF', temp_var, 'CONTINUE', loop_end))
        
        commands.extend(body_cmds)

        temp_increment = self.generate_temp_var()
        commands.append(('ADD', temp_increment, var_name, '1'))
        commands.append(('ATT', var_name, temp_increment, None))

        
        commands.append(('JUMP', loop_start, None, None))

        commands.append(('LABEL', loop_end, None, None))

        self.loop_stack.pop()

        return commands

    def procEndFor(self):
        """<endFor> -> 'IDENT' | 'NUMint' ;"""
        if self.current_token.token_type == TokenType.VARIABLE:
            value = self.current_token.lexeme
            self.eat(TokenType.VARIABLE)
            return [], value 
        elif self.current_token.token_type == TokenType.DECIMAL:
            value = self.current_token.lexeme
            self.eat(TokenType.DECIMAL)
            return [], f"'{value}'" 
        elif self.current_token.token_type == TokenType.OCTAL:
            value = self.current_token.lexeme
            self.eat(TokenType.OCTAL)
            return [], f"'{value}'" 
        else:  # HEXADECIMAL
            value = self.current_token.lexeme
            self.eat(TokenType.HEXADECIMAL)
            return [], f"'{value}'" 

    def procIoStmt(self):
        """<ioStmt> -> 'read' '(' 'IDENT' ')' ';' | 'write' '(' <outList> ')' ';' | 'readln' '(' 'IDENT' ')' ';' | 'writeln' '(' <outList> ')' ';' ;"""
        aux = []

        if self.current_token.token_type == TokenType.RESERVED_WORD_READ:
            self.eat(TokenType.RESERVED_WORD_READ)
            self.eat(TokenType.OPEN_PARENTHESES)
            var_name = self.current_token.lexeme
            self.eat(TokenType.VARIABLE)
            self.eat(TokenType.CLOSE_PARENTHESES)
            self.eat(TokenType.SEMICOLON)
            aux.append(('CALL', 'read', var_name, None))
        elif self.current_token.token_type == TokenType.RESERVED_WORD_READLN:
            self.eat(TokenType.RESERVED_WORD_READLN)
            self.eat(TokenType.OPEN_PARENTHESES)
            var_name = self.current_token.lexeme
            self.eat(TokenType.VARIABLE)
            self.eat(TokenType.CLOSE_PARENTHESES)
            self.eat(TokenType.SEMICOLON)
            aux.append(('CALL', 'read', var_name, None))  
            aux.append(('CALL', 'write','\n', None)) 
        elif self.current_token.token_type == TokenType.RESERVED_WORD_WRITE:
            self.eat(TokenType.RESERVED_WORD_WRITE)
            self.eat(TokenType.OPEN_PARENTHESES)
            aux.extend(self.procOutList())
            self.eat(TokenType.CLOSE_PARENTHESES)
            self.eat(TokenType.SEMICOLON)
        else:  # WRITELN
            self.eat(TokenType.RESERVED_WORD_WRITELN)
            self.eat(TokenType.OPEN_PARENTHESES)
            aux.extend(self.procOutList())
            aux.append(('CALL', 'write', '\n', None))
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
        """<out> -> 'STR' | 'IDENT' | 'NUMint' | 'NUMfloat' ;"""
        command = []

        if self.current_token.token_type == TokenType.STRING:
            command.append(('CALL', 'write', self.current_token.lexeme, None))
            self.eat(TokenType.STRING)
        elif self.current_token.token_type == TokenType.VARIABLE:
            command.append(('CALL', 'write', self.current_token.lexeme, None))
            self.eat(TokenType.VARIABLE)
        elif self.current_token.token_type in [TokenType.DECIMAL, TokenType.OCTAL, TokenType.HEXADECIMAL, TokenType.FLOAT]:
            command.append(('CALL', 'write', self.current_token.lexeme, None))
            self.eat(self.current_token.token_type)

        return command


    def procWhileStmt(self):
        """
            <whileStmt> -> 'while' <expr> 'do' <stmt> ;
        """
        self.eat(TokenType.RESERVED_WORD_WHILE)

        while_counter = self.generate_label()
        loop_start = f'WHILE_START_{while_counter}'
        loop_end = f'WHILE_END_{while_counter}'
        
        self.loop_stack.append({
            'start': loop_start,
            'end': loop_end,
            'type': 'WHILE'
        })
        commands = []

        commands.append(('LABEL', loop_start, None, None))
        condition_cmds, condition_result = self.procExpr()
        commands.extend(condition_cmds)
        commands.append(('IF', condition_result, 'CONTINUE', loop_end))

        self.eat(TokenType.RESERVED_WORD_DO)
        body_cmds = self.procStmt()
        commands.extend(body_cmds)
        commands.append(('JUMP', loop_start, None, None))
        commands.append(('LABEL', loop_end, None, None))
        
        self.loop_stack.pop()
        
        return commands

        
    def procIfStmt(self):
        """<ifStmt> -> 'if' <expr> 'then' <stmt> <elsePart> ;"""
        self.eat(TokenType.RESERVED_WORD_IF)
        if_counter = self.generate_label()  
        then_label = f'IF_BODY_{if_counter}'
        end_label = f'IF_END_{if_counter}'
         


        commands = []

        condition_cmds, condition_result = self.procExpr()
        commands.extend(condition_cmds)

        self.eat(TokenType.RESERVED_WORD_THEN)

        then_cmds = self.procStmt()

        else_cmds = self.procElsePart()

        if else_cmds:  
            else_label = f'IF_ELSE_{if_counter}'
            commands.append(('IF', condition_result, then_label, else_label))
            commands.append(('LABEL', then_label, None, None))
            commands.extend(then_cmds)
            commands.append(('JUMP', end_label, None, None))
            commands.append(('LABEL', else_label, None, None))
            commands.extend(else_cmds)
            commands.append(('LABEL', end_label, None, None))
        else:  
            commands.append(('IF', condition_result, then_label, end_label))
            commands.append(('LABEL', then_label, None, None))
            commands.extend(then_cmds)
            commands.append(('LABEL', end_label, None, None))

        return commands

    

    def procElsePart(self):
        """<elsePart> -> 'else' <stmt> | & ;"""
        if self.current_token.token_type == TokenType.RESERVED_WORD_ELSE:
            self.eat(TokenType.RESERVED_WORD_ELSE)
            return self.procStmt()
        else:
            return [] 
        
    def procAtrib(self):
        """<atrib> -> 'IDENT' ':=' <expr> ;"""
        var_name = self.current_token.lexeme

        self.check_variable_declared(var_name)

        self.eat(TokenType.VARIABLE)
        self.eat(TokenType.OPERATOR_ASSIGN)

        expr_cmds, expr_result = self.procExpr()

        var_type = self.get_variable_type(var_name)
        expr_type = self.get_expression_type(expr_result)


        if not self.types_compatible(var_type, expr_type):
            self.semantic_errors.append(f"Type mismatch: cannot assign {expr_type} to {var_type} variable '{var_name}'")
            raise Exception(f"Type mismatch: cannot assign {expr_type} to {var_type}")

        att_cmd = ('ATT', var_name, expr_result, None)
        return expr_cmds + [att_cmd]

    def procExpr(self):
        """<expr> -> <or> ;"""
        return self.procOr()

    def procOr(self):
        """<or> -> <and> <restoOr> ;"""
        left_cmds, left_result = self.procAnd()
        return self.procRestoOr(left_cmds, left_result)

    def procRestoOr(self, left_cmds, left_result):
        """<restoOr> -> 'or' <and> <restoOr> | & ;"""

        if self.current_token.token_type == TokenType.OPERATOR_OR:
            self.eat(TokenType.OPERATOR_OR)
            right_cmds, right_result = self.procAnd()
            
            temp_var = self.generate_temp_var()
            or_cmd = ('OR', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [or_cmd]
            return self.procRestoOr(all_cmds, temp_var)
        else:
            return left_cmds, left_result  # Sem mais operações OR

    def procAnd(self):
        """<and> -> <not> <restoAnd> ;"""
        left_cmds, left_result = self.procNot()
        return self.procRestoAnd(left_cmds, left_result)


    def procRestoAnd(self, left_cmds, left_result):
        """<restoAnd> -> 'and' <not> <restoAnd> | & ;"""

        if self.current_token.token_type == TokenType.OPERATOR_AND:
            self.eat(TokenType.OPERATOR_AND)
            right_cmds, right_result = self.procNot()
            
            temp_var = self.generate_temp_var()
            and_cmd = ('AND', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [and_cmd]
            return self.procRestoAnd(all_cmds, temp_var)
        else:
            return left_cmds, left_result  # Sem mais operações AND

    def procNot(self):
        """<not> -> 'not' <not> | <rel> ;"""
        if self.current_token.token_type == TokenType.OPERATOR_NOT:
            self.eat(TokenType.OPERATOR_NOT)
            cmds, result = self.procNot()
            
            temp_var = self.generate_temp_var()
            not_cmd = ('NOT', temp_var, result, None)
            
            return cmds + [not_cmd], temp_var
        else:
            return self.procRel()

    def procRel(self):
        """<rel> -> <add> <restoRel> ;"""
        left_cmds, left_result = self.procAdd()
        return self.procRestoRel(left_cmds, left_result)

    def procRestoRel(self, left_cmds, left_result):
        """<restoRel> -> '==' <add> | '' <add> | '<' <add> | '<=' <add> | '>' <add> | '>=' <add> | & ;"""

        if self.current_token.token_type == TokenType.OPERATOR_EQUAL:
            self.eat(TokenType.OPERATOR_EQUAL)
            right_cmds, right_result = self.procAdd()
            
            temp_var = self.generate_temp_var()
            eq_cmd = ('EQ', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [eq_cmd]
            return all_cmds, temp_var
            
        elif self.current_token.token_type == TokenType.OPERATOR_NOT_EQUAL:
            self.eat(TokenType.OPERATOR_NOT_EQUAL)
            right_cmds, right_result = self.procAdd()
            
            temp_var = self.generate_temp_var()
            neq_cmd = ('NEQ', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [neq_cmd]
            return all_cmds, temp_var
            
        elif self.current_token.token_type == TokenType.OPERATOR_LESS:
            self.eat(TokenType.OPERATOR_LESS)
            right_cmds, right_result = self.procAdd()
            
            temp_var = self.generate_temp_var()
            less_cmd = ('LESS', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [less_cmd]
            return all_cmds, temp_var
            
        elif self.current_token.token_type == TokenType.OPERATOR_LESS_EQUAL:
            self.eat(TokenType.OPERATOR_LESS_EQUAL)
            right_cmds, right_result = self.procAdd()
            
            temp_var = self.generate_temp_var()
            leq_cmd = ('LEQ', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [leq_cmd]
            return all_cmds, temp_var
            
        elif self.current_token.token_type == TokenType.OPERATOR_GREATER:
            self.eat(TokenType.OPERATOR_GREATER)
            right_cmds, right_result = self.procAdd()
            
            temp_var = self.generate_temp_var()
            gret_cmd = ('GRET', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [gret_cmd]
            return all_cmds, temp_var
            
        elif self.current_token.token_type == TokenType.OPERATOR_GREATER_EQUAL:
            self.eat(TokenType.OPERATOR_GREATER_EQUAL)
            right_cmds, right_result = self.procAdd()
            
            temp_var = self.generate_temp_var()
            geq_cmd = ('GEQ', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [geq_cmd]
            return all_cmds, temp_var
        else:
            return left_cmds, left_result  # Sem comparação

    def procAdd(self):
        """<add> -> <mult> <restoAdd> ;"""
        left_cmds, left_result = self.procMult()
        return self.procRestoAdd(left_cmds, left_result)

    def procRestoAdd(self, left_cmds, left_result):
        """<restoAdd> -> '+' <mult> <restoAdd> | '-' <mult> <restoAdd> | & """

        if self.current_token.token_type == TokenType.OPERATOR_PLUS:
            self.eat(TokenType.OPERATOR_PLUS)
            right_cmds, right_result = self.procMult()
            
            temp_var = self.generate_temp_var()
            add_cmd = ('ADD', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [add_cmd]
            return self.procRestoAdd(all_cmds, temp_var)
            
        elif self.current_token.token_type == TokenType.OPERATOR_MINUS:
            self.eat(TokenType.OPERATOR_MINUS)
            right_cmds, right_result = self.procMult()
            
            temp_var = self.generate_temp_var()
            sub_cmd = ('SUB', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [sub_cmd]
            return self.procRestoAdd(all_cmds, temp_var)
        else:
            return left_cmds, left_result  # Sem mais operações
        
    def procMult(self):
        """<mult> -> <uno> <restoMult> ;"""
        left_cmds, left_result = self.procUno()
        return self.procRestoMult(left_cmds, left_result)

    def procRestoMult(self, left_cmds, left_result):
        """<restoMult> -> '*' <uno> <restoMult> | '/' <uno> <restoMult> | 'mod' <uno> <restoMult> | 'div' <uno> <restoMult> | & ;"""

        if self.current_token.token_type == TokenType.OPERATOR_MULTIPLY:
            self.eat(TokenType.OPERATOR_MULTIPLY)
            right_cmds, right_result = self.procUno()
            
            temp_var = self.generate_temp_var()
            mult_cmd = ('MULT', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [mult_cmd]
            return self.procRestoMult(all_cmds, temp_var)
            
        elif self.current_token.token_type == TokenType.OPERATOR_DIVIDE:
            self.eat(TokenType.OPERATOR_DIVIDE)
            right_cmds, right_result = self.procUno()
            
            temp_var = self.generate_temp_var()
            div_cmd = ('DIV', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [div_cmd]
            return self.procRestoMult(all_cmds, temp_var)
            
        elif self.current_token.token_type == TokenType.OPERATOR_MOD:
            self.eat(TokenType.OPERATOR_MOD)
            right_cmds, right_result = self.procUno()
            
            temp_var = self.generate_temp_var()
            mod_cmd = ('MOD', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [mod_cmd]
            return self.procRestoMult(all_cmds, temp_var)
            
        elif self.current_token.token_type == TokenType.OPERATOR_INTEGER_DIVIDER:
            self.eat(TokenType.OPERATOR_INTEGER_DIVIDER)
            right_cmds, right_result = self.procUno()
            
            temp_var = self.generate_temp_var()
            idiv_cmd = ('IDIV', temp_var, left_result, right_result)
            
            all_cmds = left_cmds + right_cmds + [idiv_cmd]
            return self.procRestoMult(all_cmds, temp_var)
        else:
            return left_cmds, left_result  # Sem mais operações
    def procUno(self):
        """<uno> -> '+' <uno> | '-' <uno> | <fator> ;"""
        if self.current_token.token_type == TokenType.OPERATOR_PLUS:
            self.eat(TokenType.OPERATOR_PLUS)
            return self.procUno()  # +5 é igual a 5
        elif self.current_token.token_type == TokenType.OPERATOR_MINUS:
            self.eat(TokenType.OPERATOR_MINUS)
            cmds, result = self.procUno()
            
            # Para -numero, fazemos SUB(temp, 0, numero)
            temp_var = self.generate_temp_var()
            sub_cmd = ('SUB', temp_var, '0', result)
            
            return cmds + [sub_cmd], temp_var
        else:
            return self.procFactor()

    def procFactor(self):
        """<fator> -> 'NUMint' | 'NUMfloat' | 'IDENT' | '(' <expr> ')' | 'STR' ;"""
        if self.current_token.token_type == TokenType.DECIMAL:
            value = self.current_token.lexeme
            self.eat(TokenType.DECIMAL)
            return [], f"'{value}'" 
        elif self.current_token.token_type == TokenType.OCTAL:
            value = self.current_token.lexeme
            self.eat(TokenType.OCTAL)
            return [], f"'{value}' " 
        elif self.current_token.token_type == TokenType.HEXADECIMAL:
            value = self.current_token.lexeme
            self.eat(TokenType.HEXADECIMAL)
            return [], f"'{value}' "
        elif self.current_token.token_type == TokenType.FLOAT:
            value = self.current_token.lexeme
            self.eat(TokenType.FLOAT)
            return [], f"'{value}' " 
        elif self.current_token.token_type == TokenType.VARIABLE:
            value = self.current_token.lexeme
            self.eat(TokenType.VARIABLE)
            return [], value 
        elif self.current_token.token_type == TokenType.OPEN_PARENTHESES:
            self.eat(TokenType.OPEN_PARENTHESES)
            expr_cmds, expr_result = self.procExpr()
            self.eat(TokenType.CLOSE_PARENTHESES)
            return expr_cmds, expr_result
        else:  # STRING
            value = self.current_token.lexeme
            self.eat(TokenType.STRING)
            return [], value