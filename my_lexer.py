import logging
from my_token import TokenType, Token


def build_keywords():
    token_list = list(TokenType)
    start_index = token_list.index(TokenType.BEGIN)
    end_index = token_list.index(TokenType.END)
    reserved_keywords = {
        token_type.value: token_type for token_type in token_list[start_index:end_index + 1]
    }
    return reserved_keywords


RESERVED_KEYWORDS = build_keywords()


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.column = 1

    def move(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

    def lookup(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                return self.ident()
            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.number())
            if self.current_char == ':' and self.lookup() == '=':
                token = Token(
                    type=TokenType.ASSIGN,
                    value=TokenType.ASSIGN.value,  # ':='
                    line=self.line,
                    column=self.column,
                )
                self.move()
                self.move()
                return token

            try:
                token_type = TokenType(self.current_char)
            except ValueError:
                logging.error(self.error())
            else:
                token = Token(
                    type=token_type,
                    value=token_type.value,
                    line=self.line,
                    column=self.column,
                )
                self.move()
                return token

        return Token(TokenType.EOF, None)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.move()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.move()
        return int(result)

    def ident(self):
        token = Token(type=None, value=None, line=self.line, column=self.column)
        value = ''
        while self.current_char is not None and self.current_char.isalnum():
            value += self.current_char
            self.move()
        token_type = RESERVED_KEYWORDS.get(value.upper())
        if token_type is None:
            token.type = TokenType.ID
            token.value = value
        else:
            token.type = token_type
            token.value = value.upper()

        return token
