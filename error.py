from enum import Enum


class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'


class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        self.error_code = error_code
        self.token = token
        # add exception class name before the message
        self.message = message


class LexerError(Error):
    pass

class ParserError(Error):
    pass

