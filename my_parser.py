from error import ParserError, ErrorCode
from token import TokenType


class AST(object):
    pass


class Program(AST):
    """Represents a 'BEGIN ... END' block"""

    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    """The Var node is constructed out of ID token."""

    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def get_next_token(self):
        return self.lexer.get_next_token()

    def error(self, error_code, token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        print('EXP', token_type, "CURR", self.current_token.type)
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )

    def program_body(self):
        """
        compound_statement: BEGIN statement_list END
        """
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Program()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement
                       | statement statement_list
        """
        node = self.statement()
        results = [node]

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())

        if self.current_token.type == TokenType.ID:
            self.error()

        return results

    def id_list(self):
        """
        id_list : variable
                | variable id_list
        """
        node = self.variable()
        results = [node]

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            results.append(self.variable())

        return results

    def expr_list(self):
        """
        id_list : expr
                | expr expr_list
        """
        node = self.expr()
        results = [node]

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            results.append(self.expr())

        return results

    def statement(self):
        """
        statement : read_statement
                  | write_statement
                  | if_statement
                  | assign_statement
        """
        if self.current_token.type == TokenType.READ:
            node = self.read_statement()
        elif self.current_token.type == TokenType.WRITE:
            node = self.write_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.if_statement()
        elif self.current_token.type == TokenType.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def read_statement(self):
        """
        read_statement : READ ( id_list );
        """
        self.eat(TokenType.READ)
        self.eat(TokenType.LPAREN)
        nodes = self.id_list()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMI)
        # input(nodes)

    def write_statement(self):
        """
        read_statement : READ ( id_list );
        """
        self.eat(TokenType.WRITE)
        self.eat(TokenType.LPAREN)
        nodes = self.expr_list()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMI)
        # print(nodes)

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def term(self):
        """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        node = self.factor()

        return node

    def factor(self):
        """factor : PLUS  factor
              | MINUS factor
              | INTEGER
              | LPAREN expr RPAREN
              | variable
        """
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        node = self.program_body()
        if self.current_token.type != TokenType.EOF:
            print('NOT EOF')
            self.error()

        print('FINISH')
        return node
