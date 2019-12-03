from enum import Enum


class TokenType(Enum):
    # single-character token types
    PLUS = '+'
    MINUS = '-'
    LPAREN = '('
    RPAREN = ')'
    SEMI = ';'
    COMMA = ','
    # block of reserved words
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
    END = 'END'  # marks the end of the block
    # misc
    ID = 'ID'
    INTEGER = 'INTEGER'
    ASSIGN = ':='
    EOF = 'EOF'
