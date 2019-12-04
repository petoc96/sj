import io
from my_lexer import Lexer
from my_parser import Parser


def main():
    with io.open("input_correct.txt", 'r') as fin:
        text = fin.read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    parser.parse()


if __name__ == '__main__':
    main()
