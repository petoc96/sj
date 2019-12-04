from my_token import TokenType
import logging

logging.basicConfig(level=logging.INFO)


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def get_next_token(self):
        return self.lexer.get_next_token()

    def process(self, token_type):
        if self.current_token.type == token_type:
            logging.info('Parsing token: ' + str(self.current_token))
            self.current_token = self.get_next_token()
        else:
            logging.error('Unexpected token: ' + str(self.current_token) + '. Consider using token: ' + str(token_type))
            exit()

    def program(self):
        # program: BEGIN statement_list END
        logging.info('Creating node PROGRAM')
        self.process(TokenType.BEGIN)
        self.statement_list()
        self.process(TokenType.END)
        logging.info('Leaving node PROGRAM')

    def statement_list(self):
        # statement_list : statement
        #                | statement statement_list
        logging.info('Creating node STATEMENT_LIST')
        self.statement()
        while self.current_token.type == TokenType.SEMI:
            self.process(TokenType.SEMI)
            self.statement()
        logging.info('Leaving node STATEMENT_LIST')

    def id_list(self):
        # id_list : variable
        #         | variable id_list
        logging.info('Creating node ID_LIST')
        self.ident()
        while self.current_token.type == TokenType.COMMA:
            self.process(TokenType.COMMA)
            self.ident()
        logging.info('Leaving node ID_LIST')

    def expr_list(self):
        # id_list : expr
        #         | expr expr_list
        logging.info('Creating node EXPR_LIST')
        self.expr()
        while self.current_token.type == TokenType.COMMA:
            self.process(TokenType.COMMA)
            self.expr()
        logging.info('Leaving node EXPR_LIST')

    def statement(self):
        # statement : read_statement
        #           | write_statement
        #           | if_statement
        #           | assign_statement
        logging.info('Creating node STATEMENT')
        if self.current_token.type == TokenType.READ:
            self.read_statement()
        elif self.current_token.type == TokenType.WRITE:
            self.write_statement()
        elif self.current_token.type == TokenType.IF:
            self.if_statement()
        elif self.current_token.type == TokenType.ID:
            self.assignment_statement()
        logging.info('Leaving node STATEMENT')

    def bfactor(self):
        # bfactor : NOT bfactor
        #         | ( bexpr )
        #         | TRUE
        #         | FALSE
        logging.info('Creating node BFACTOR')
        if self.current_token.type == TokenType.NOT:
            self.process(TokenType.NOT)
            self.bfactor()
        elif self.current_token.type == TokenType.LPAREN:
            self.process(TokenType.LPAREN)
            self.bexpr()
            self.process(TokenType.RPAREN)
        elif self.current_token.type == TokenType.TRUE:
            self.process(TokenType.TRUE)
        elif self.current_token.type == TokenType.FALSE:
            self.process(TokenType.FALSE)
        else:
            logging.error('Unexpected token: ' + str(self.current_token))
            exit()
        logging.info('Leaving node BFACTOR')

    def bterm(self):
        # bterm : bfactor
        #      | bfactor AND bfactor
        logging.info('Creating node BTERM')
        self.bfactor()
        while self.current_token.type == TokenType.AND:
            self.process(TokenType.AND)
            self.bfactor()
        logging.info('Leaving node BTERM')

    def bexpr(self):
        # bexpr : bterm
        #       | bterm OR bterm
        logging.info('Creating node BEXPR')
        self.bterm()
        while self.current_token.type == TokenType.OR:
            self.process(TokenType.OR)
            self.bterm()

    def if_statement(self):
        # if_statement : IF bexpr THEN statement;
        #              | IF bexpr THEN statement ELSE statement;
        logging.info('Creating node IF_STATEMENT')
        self.process(TokenType.IF)
        self.bexpr()
        self.process(TokenType.THEN)
        self.statement()
        self.process(TokenType.SEMI)
        if self.current_token.type == TokenType.ELSE:
            self.process(TokenType.ELSE)
            self.statement()
        logging.info('Leaving node IF_STATEMENT')

    def read_statement(self):
        # read_statement : READ ( id_list );
        logging.info('Creating node READ_STATEMENT')
        self.process(TokenType.READ)
        self.process(TokenType.LPAREN)
        self.id_list()
        self.process(TokenType.RPAREN)
        if self.current_token.type != TokenType.SEMI:
            logging.error('Missing token: ' + str(TokenType.SEMI) + ' at position ' +
                          str(self.current_token.line) + ':' + str(self.current_token.column-1))
            exit()
        logging.info('Leaving node READ_STATEMENT')

    def write_statement(self):
        # read_statement : READ ( id_list );
        logging.info('Creating node WRITE_STATEMENT')
        self.process(TokenType.WRITE)
        self.process(TokenType.LPAREN)
        self.expr_list()
        self.process(TokenType.RPAREN)
        if self.current_token.type != TokenType.SEMI:
            logging.error('Missing token: ' + str(TokenType.SEMI) + ' at position ' +
                          str(self.current_token.line) + ':' + str(self.current_token.column-1))
            exit()
        logging.info('Leaving node WRITE_STATEMENT')

    def assignment_statement(self):
        # assignment_statement : variable ASSIGN expr
        logging.info('Creating node ASSIGN_STATEMENT')
        self.ident()
        self.process(TokenType.ASSIGN)
        self.expr()
        if self.current_token.type != TokenType.SEMI:
            logging.error('Missing token: ' + str(TokenType.SEMI) + ' at position ' +
                          str(self.current_token.line) + ':' + str(self.current_token.column-1))
            exit()
        logging.info('Leaving node ASSIGN_STATEMENT')

    def ident(self):
        # variable : ID
        logging.info('Creating node IDENT')
        self.process(TokenType.ID)
        logging.info('Leaving node IDENT')

    def factor(self):
        # factor : PLUS  number
        #       | MINUS number
        #       | number
        #       | ( expr )
        #       | variable
        logging.info('Creating node FACTOR')
        if self.current_token.type == TokenType.PLUS:
            self.process(TokenType.PLUS)
            self.process(TokenType.NUMBER)
        elif self.current_token.type == TokenType.MINUS:
            self.process(TokenType.MINUS)
            self.process(TokenType.NUMBER)
        elif self.current_token.type == TokenType.NUMBER:
            self.process(TokenType.NUMBER)
        elif self.current_token.type == TokenType.LPAREN:
            self.process(TokenType.LPAREN)
            self.expr()
            self.process(TokenType.RPAREN)
        else:
            self.ident()
        logging.info('Leaving node FACTOR')

    def expr(self):
        # expr : factor
        #      | factor op factor
        logging.info('Creating node EXPRESSION')
        self.factor()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.process(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.process(TokenType.MINUS)
            self.factor()
        logging.info('Leaving node EXPRESSION')

    def parse(self):
        logging.info('Building parsing tree')
        self.program()
        if self.current_token.type != TokenType.EOF:
            logging.error('Unexpected token after end of program: ' + str(self.current_token))
            exit()
        logging.info('Finished parsing')
