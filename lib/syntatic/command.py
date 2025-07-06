from enum import Enum, auto


class Command(Enum):
    ATT = auto()  # Atribuição

    ADD = auto()  # Adição
    SUB = auto()  # Subtração
    MULT = auto()  # Multiplicação
    IDIV = auto()  # Divisão inteira
    DIV = auto()  # Divisão
    MOD = auto()  # Módulo

    IF = auto()  # Condicional
    JUMP = auto()  # Pular para outra instrução
    LABEL = auto()  # Rótulo para salto

    EQ = auto()  # =
    NEQ = auto()  # !=
    LEQ = auto()  # <=
    LESS = auto()  # <
    GEQ = auto()  # >=
    GRET = auto()  # >

    CALL = auto()  # Chamada de função

    OR = auto()  # Operador lógico OU
    AND = auto()  # Operador lógico E
    NOT = auto()  # Operador lógico NÃO
