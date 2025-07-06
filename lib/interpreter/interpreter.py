class Interpreter:
    def __init__(self, instructions):
        self.instructions = instructions
        self.variables = {}  # Armazena as variáveis do programa
        self.pc = 0  # Program counter - índice da instrução atual
        self.labels = {}  # Mapeia labels para posições no código
        self.loop_stack = []  # Pilha de blocos de loop (início e fim)

    def run(self):
        """Executa o programa intermediário"""
        # Primeiro passo: identificar todas as labels
        self._map_labels()

        # Segundo passo: executar as instruções
        self.pc = 0
        while self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            self._execute_instruction(instruction)

            # Não incrementamos o pc se a instrução era um jump ou if
            # pois esses comandos já ajustam o pc diretamente
            if instruction[2] not in ['JUMP', 'IF', 'BREAK', 'CONTINUE']:
                self.pc += 1

    def _map_labels(self):
        """Mapeia todas as labels para suas posições no código"""
        for i, instruction in enumerate(self.instructions):
            if instruction[0] == 'LABEL':
                self.labels[instruction[1]] = i

    def _try_convert_to_number(self, value: str):

        if "." in str(value):
            try:
                return float(value)
            except ValueError:
                return value

        try:
            return int(value)
        except ValueError:
            return value

    def _get_value(self, operand):
        """Obtém o valor de um operando (variável ou literal)"""
        if operand is None:
            return None

        # Se é uma string que representa um número
        if isinstance(operand, str) and operand.startswith("'") and operand.endswith("'"):
            return self._try_convert_to_number(operand[1:-1])

        # Se é uma string literal com aspas duplas
        elif isinstance(operand, str) and operand.startswith('"') and operand.endswith('"'):
            return operand[1:-1]  # Remove as aspas

        # Se está nas variáveis, pega o valor
        elif isinstance(operand, str) and operand in self.variables:
            return self._try_convert_to_number(self.variables[operand])

        # Para caracteres especiais como '\n'
        elif operand == '\\n':
            return '\n'

        # Caso contrário, retorna o operando como está
        return self._try_convert_to_number(operand)

    def _execute_instruction(self, instruction):
        """Executa uma instrução individual"""
        cmd = instruction[0]

        try:
            if cmd == 'ATT':
                self._execute_att(instruction)
            elif cmd == 'ADD':
                self._execute_add(instruction)
            elif cmd == 'SUB':
                self._execute_sub(instruction)
            elif cmd == 'IF':
                self._execute_if(instruction)
            elif cmd == 'JUMP':
                self._execute_jump(instruction)
            elif cmd == 'LABEL':
                # Labels já foram processados na fase de mapeamento
                pass
            elif cmd == 'EQ':
                self._execute_eq(instruction)
            elif cmd == 'NEQ':
                self._execute_neq(instruction)
            elif cmd == 'LEQ':
                self._execute_leq(instruction)
            elif cmd == 'GEQ':
                self._execute_geq(instruction)
            elif cmd == 'GRET':
                self._execute_gret(instruction)
            elif cmd == 'LESS':
                self._execute_less(instruction)
            elif cmd == 'MULT':
                self._execute_mult(instruction)
            elif cmd == 'IDIV':
                self._execute_idiv(instruction)
            elif cmd == 'DIV':
                self._execute_div(instruction)
            elif cmd == 'MOD':
                self._execute_mod(instruction)
            elif cmd == 'CALL':
                self._execute_call(instruction)
            elif cmd == 'OR':
                self._execute_or(instruction)
            elif cmd == 'AND':
                self._execute_and(instruction)
            elif cmd == 'NOT':
                self._execute_not(instruction)
            elif cmd == 'BREAK':
                self._execute_break(instruction)
            elif cmd == 'CONTINUE':
                self._execute_continue(instruction)
            else:
                print(f"Comando desconhecido: {cmd}")
        except Exception as e:
            print(f"Erro ao executar {instruction}: {e}")
            raise

    def _execute_att(self, instruction):
        """Atribuição: ('ATT', SALVO, VALOR, NONE)"""
        variable = instruction[1]
        value = self._get_value(instruction[2])
        self.variables[variable] = value

    def _execute_add(self, instruction):
        """Adição: ('ADD', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = op1 + op2

    def _execute_sub(self, instruction):
        """Subtração: ('SUB', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = op1 - op2

    def _execute_if(self, instruction):
        """Condicional: ('IF', COND, LABEL_TRUE, LABEL_FALSE)"""
        condition = self._get_value(instruction[1])
        if condition:
            self.pc = self.labels[instruction[2]]
        else:
            self.pc = self.labels[instruction[3]]

    def _execute_jump(self, instruction):
        """Salto: ('JUMP', LABEL, NONE, NONE)"""
        self.pc = self.labels[instruction[1]]

    def _execute_break(self, instruction):
        """Break: ('BREAK', None, None, None)"""
        if not self.loop_stack:
            raise RuntimeError("Instrução BREAK fora de um loop")

        # Salta para o fim do loop atual
        end_label = self.loop_stack[-1][1]
        self.pc = self.labels[end_label]

    def _execute_continue(self, instruction):
        """Continue: ('CONTINUE', None, None, None)"""
        if not self.loop_stack:
            raise RuntimeError("Instrução CONTINUE fora de um loop")

        # Salta para o início do loop atual
        start_label = self.loop_stack[-1][0]
        self.pc = self.labels[start_label]

    def _execute_eq(self, instruction):
        """Igualdade: ('EQ', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = 1 if op1 == op2 else 0

    def _execute_neq(self, instruction):
        """Desigualdade: ('NEQ', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = 1 if op1 != op2 else 0

    def _execute_leq(self, instruction):
        """Menor ou igual: ('LEQ', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = 1 if op1 <= op2 else 0

    def _execute_geq(self, instruction):
        """Maior ou igual: ('GEQ', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = 1 if op1 >= op2 else 0

    def _execute_gret(self, instruction):
        """Maior que: ('GRET', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = 1 if op1 > op2 else 0

    def _execute_less(self, instruction):
        """Menor que: ('LESS', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = 1 if op1 < op2 else 0

    def _execute_mult(self, instruction):
        """Multiplicação: ('MULT', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = op1 * op2

    def _execute_idiv(self, instruction):
        """Divisão inteira: ('IDIV', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        if op2 == 0:
            raise ZeroDivisionError("Divisão por zero")
        self.variables[result_var] = op1 // op2

    def _execute_div(self, instruction):
        """Divisão: ('DIV', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        if op2 == 0:
            raise ZeroDivisionError("Divisão por zero")
        self.variables[result_var] = op1 / op2

    def _execute_mod(self, instruction):
        """Módulo: ('MOD', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        if op2 == 0:
            raise ZeroDivisionError("Módulo por zero")
        self.variables[result_var] = op1 % op2

    def _execute_or(self, instruction):
        """Operação OR: ('OR', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = 1 if (op1 or op2) else 0

    def _execute_and(self, instruction):
        """Operação AND: ('AND', SALVO, OP1, OP2)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        op2 = self._get_value(instruction[3])
        self.variables[result_var] = 1 if (op1 and op2) else 0

    def _execute_not(self, instruction):
        """Operação NOT: ('NOT', SALVO, OP1, NONE)"""
        result_var = instruction[1]
        op1 = self._get_value(instruction[2])
        self.variables[result_var] = 1 if not op1 else 0

    def _execute_call(self, instruction):
        """Chamada de função: ('CALL', 'read'/'write', SALVO/ESCRITO, NONE)"""
        function = instruction[1]

        if function == 'read':
            var = instruction[2]
            try:
                value = input()
                # Tenta converter para int ou float
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # Deixa como string se não for número
                self.variables[var] = value
            except Exception as e:
                print(f"Erro na leitura: {e}")

        elif function == 'readln':
            var = instruction[2]
            try:
                value = input()
                # Tenta converter para int ou float
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # Deixa como string se não for número
                self.variables[var] = value
            except Exception as e:
                print(f"Erro na leitura: {e}")

        elif function == 'write':
            value = self._get_value(instruction[2])
            print(value, end="")

    def _start_loop(self, start_label, end_label):
        """Registra o início de um loop"""
        self.loop_stack.append((start_label, end_label))

    def _end_loop(self):
        """Registra o fim de um loop"""
        if self.loop_stack:
            self.loop_stack.pop()
