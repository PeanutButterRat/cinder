import os
import subprocess
import sys
from tempfile import NamedTemporaryFile

from llvmlite import binding

from cinder import parser
from cinder.ast import transformer
from cinder.visitors import ASTCompiler, ASTVerifier


def main():
    if len(sys.argv) != 2:
        print("usage: cinder <string>")
        sys.exit(1)

    source = sys.argv[1]

    try:
        compile(source)
    except Exception as e:
        print(f"Error: {e}")


def compile(source):
    cst = parser.parse(source)
    ast = transformer.transform(cst)
    ASTVerifier().visit(ast)
    module = ASTCompiler().visit(ast)

    binding.initialize()
    binding.initialize_native_target()
    binding.initialize_native_asmprinter()

    target = binding.Target.from_default_triple()
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
