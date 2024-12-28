import sys

from llvmlite import binding, ir

from cinder import parser
from cinder.ast import transformer


def main():
    if len(sys.argv) != 2:
        print("usage: cinder <string>")
        sys.exit(1)

    source = sys.argv[1]
    cst = parser.parse(source)
    ast = transformer.transform(cst)

    module = ir.Module()
    entry = ir.Function(module, ir.FunctionType(ir.IntType(32), []), "main")
    block = entry.append_basic_block()
    builder = ir.IRBuilder(block)

    ast.compile(builder)

    print(module)


if __name__ == "__main__":
    main()
