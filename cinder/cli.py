import argparse
import os
import subprocess
import traceback
from tempfile import NamedTemporaryFile

from llvmlite import binding
from llvmlite.binding import Target

from cinder import parser
from cinder.ast import transformer
from cinder.visitors import ASTCompiler, ASTVerifier


def main():
    argparser = argparse.ArgumentParser(
        prog="cinder", description="A low-level systems programming language."
    )
    argparser.add_argument("source", help="source string to compile")
    argparser.add_argument(
        "-a",
        "--show-ast",
        action="store_true",
        help="show the abstract syntax tree (AST) before attempting to compile",
    )
    argparser.add_argument(
        "-t", "--target", help="platform to compile for specified as a target triple"
    )
    argparser.add_argument(
        "-s",
        "--stack-trace",
        help="print the stack trace if an exception is raised",
        action="store_true",
    )

    args = argparser.parse_args()

    try:
        ast = parse(args.source)

        if args.show_ast:
            print(ast.pretty())

        target = args.target if args.target else "default"
        compile(ast, target)

    except Exception as e:
        if args.stack_trace:
            traceback.print_exc()
        else:
            print(f"Error: {e}")


def parse(source):
    cst = parser.parse(source)
    ast = transformer.transform(cst)
    ASTVerifier().visit(ast)
    return ast


def compile(ast, target="default"):
    module = ASTCompiler().visit(ast)

    binding.initialize()
    binding.initialize_native_target()
    binding.initialize_native_asmprinter()

    if target == "default":
        target = Target.from_default_triple()
    else:
        target = Target.from_triple(target)

    machine = target.create_target_machine(codemodel="default")
    module = binding.parse_assembly(str(module))

    with NamedTemporaryFile(delete=False) as file:
        file.write(machine.emit_object(module))

    os.makedirs("build", exist_ok=True)
    output = os.path.join("build", "output.exe")

    subprocess.run(["gcc", "-o", output, file.name])

    try:
        os.remove(file.name)
    except:
        pass


if __name__ == "__main__":
    main()
