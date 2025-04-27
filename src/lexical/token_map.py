from lexical.token_type import TokenType


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
    "mod": TokenType.OPERATOR_MOD,
    "div": TokenType.OPERATOR_INTEGER_DIVIDER,
    "and": TokenType.OPERATOR_AND,
    "or": TokenType.OPERATOR_OR,
    "not": TokenType.OPERATOR_NOT
}