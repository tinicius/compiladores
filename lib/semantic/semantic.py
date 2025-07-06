class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}     
        self.current_scope = 'global'  
        self.errors = []         
        
    def analyze(self, intermediate_code):
        """Analisa o código intermediário"""
        try:
            self.build_symbol_table(intermediate_code)
            self.check_semantics(intermediate_code)
            
            if self.errors:
                raise Exception(f"Semantic errors found: {self.errors}")
                
            return True
        except Exception as e:
            print(f"Semantic Analysis Error: {e}")
            return False
        
    def check_semantics(self, intermediate_code):
        """Verifica a semântica do código intermediário"""
        for cmd in intermediate_code:
            if cmd[0] == 'ATT':  # Atribuição
                self.check_assignment(cmd)
            elif cmd[0] in ['ADD', 'SUB', 'MULT', 'DIV']:
                self.check_arithmetic_operation(cmd)
            elif cmd[0] in ['EQ', 'NEQ', 'LESS', 'GRET', 'LEQ', 'GEQ']:
                self.check_comparison_operation(cmd)
            elif cmd[0] in ['AND', 'OR', 'NOT']:
                self.check_logical_operation(cmd)

    def check_assignment(self, cmd):
        """Verifica compatibilidade na atribuição"""
        var_name = cmd[1]
        value = cmd[2]

        # Verificar se variável foi declarada
        if var_name not in self.symbol_table:
            self.errors.append(f"Variable '{var_name}' not declared")
            return

        # Verificar tipos compatíveis
        var_type = self.symbol_table[var_name]['type']
        value_type = self.get_expression_type(value)

        if not self.types_compatible(var_type, value_type):
            self.errors.append(f"Type mismatch: cannot assign {value_type} to {var_type}")
    
    def get_expression_type(self, expression):
        """Determina o tipo de uma expressão"""
        if isinstance(expression, str):
            if expression.startswith("'") and expression.endswith("'"):
                # É um literal numérico
                value = expression[1:-1]
                if '.' in value:
                    return 'real'
                else:
                    return 'integer'
            elif expression.startswith('"') and expression.endswith('"'):
                # É uma string literal
                return 'string'
            else:
                # É uma variável
                return self.get_variable_type(expression)
            return 'unknown'

    def types_compatible(self, type1, type2):
        """Verifica se dois tipos são compatíveis"""
        if type1 == type2:
            return True

        # integer pode ser atribuído a real
        if type1 == 'real' and type2 == 'integer':
            return True
            
        return False

    def check_arithmetic_operation(self, cmd):
        """Verifica operações aritméticas"""
        op1_type = self.get_expression_type(cmd[2])
        op2_type = self.get_expression_type(cmd[3])

        if op1_type not in ['integer', 'real'] or op2_type not in ['integer', 'real']:
            self.errors.append(f"Arithmetic operation requires numeric types")
            
    def check_comparison_operation(self, cmd):
        """Verifica operações de comparação"""
        op1_type = self.get_expression_type(cmd[2])
        op2_type = self.get_expression_type(cmd[3])

        if not self.types_compatible(op1_type, op2_type):
            self.errors.append(f"Cannot compare {op1_type} with {op2_type}")

    def check_logical_operation(self, cmd):
        """Verifica operações lógicas"""
        if cmd[0] == 'NOT':
            op_type = self.get_expression_type(cmd[2])
            if op_type != 'boolean':
                self.errors.append(f"Logical NOT requires boolean type, got {op_type}")
        else:  # AND, OR
            op1_type = self.get_expression_type(cmd[2])
            op2_type = self.get_expression_type(cmd[3])
            
            if op1_type != 'boolean' or op2_type != 'boolean':
                self.errors.append(f"Logical operations require boolean types")

    def print_symbol_table(self):
        """Imprime a tabela de símbolos para debug"""
        print("\n=== SYMBOL TABLE ===")
        for name, info in self.symbol_table.items():
            print(f"{name}: {info['type']} (scope: {info['scope']})")
            
    def build_symbol_table(self, intermediate_code):
        """Constrói tabela de símbolos a partir das declarações"""
        for cmd in intermediate_code:
            if cmd[0] == 'DECLARE':  
                var_name = cmd[1]
                var_type = cmd[2]
                
                if var_name in self.symbol_table:
                    self.errors.append(f"Variable '{var_name}' already declared")
                else:
                    self.symbol_table[var_name] = {
                        'type': var_type,  
                        'initialized': False,
                        'scope': self.current_scope
                    }

    def get_variable_type(self, var_name):
        """Retorna o tipo de uma variável"""
        if var_name in self.symbol_table:
            return self.symbol_table[var_name]['type']
        else:
            # Se não encontrou, assumir que é integer (temporário)
            return 'integer'