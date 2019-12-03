import io
from lexer import Lexer
from my_parser import Parser


def main():
    with io.open("input.txt", 'r') as fin:
        text = fin.read()
    text = "BEGIN write(7+7); END"
    lexer = Lexer(text)
    parser = Parser(lexer)
    parser.parse()
    print('EXIT')


if __name__ == '__main__':
    main()
