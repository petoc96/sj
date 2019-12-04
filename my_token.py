from enum import Enum


class TokenType(Enum):
    PLUS = '+'
    MINUS = '-'
    LPAREN = '('
    RPAREN = ')'
    SEMI = ';'
    COMMA = ','
    #
    BEGIN = 'BEGIN'
    READ = 'READ'
    WRITE = 'WRITE'
    IF = 'IF'
    ELSE = 'ELSE'
    THEN = 'THEN'
    OR = 'OR'
    AND = 'AND'
    NOT = 'NOT'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    END = 'END'
    #
    ID = 'ID'
    NUMBER = 'NUMBER'
    ASSIGN = ':='
    EOF = 'EOF'


class Token(object):
    def __init__(self, type, value, line=None, column=None):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return 'Token({type}, {value}, position={lineno}:{column})'.format(
            type=self.type,
            value=str(self.value),
            lineno=self.line,
            column=self.column,
        )
