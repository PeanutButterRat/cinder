import sys

from cinder import parser
from cinder.ast import transformer


def main():
    if len(sys.argv) != 2:
        print("usage: cinder <string>")
        sys.exit(1)

    source = sys.argv[1]
    cst = parser.parse(source)
    ast = transformer.transform(cst)

    print(ast.pretty())


if __name__ == "__main__":
    main()
