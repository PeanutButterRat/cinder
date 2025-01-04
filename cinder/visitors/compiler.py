from llvmlite import ir

from cinder.ast import _Node
from cinder.symbols import Symbols
from cinder.visitors.visitor import Interpreter


class ASTCompiler(Interpreter):
    def __init__(self):
        super().__init__()
        self.symbols = Symbols()
        self.module = ir.Module()

        entry = ir.Function(self.module, ir.FunctionType(ir.IntType(32), []), "main")
        block = entry.append_basic_block()
        self.builder = ir.IRBuilder(block)

        printf = ir.Function(
            self.module,
            ir.FunctionType(
                ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True
            ),
            name="printf",
        )

        format = ir.GlobalVariable(
            self.module, ir.ArrayType(ir.IntType(8), count=4), name="format"
        )
        format.global_constant = True
        format.initializer = ir.Constant(
            ir.ArrayType(ir.IntType(8), count=4),
            bytearray("%d\n".encode("utf8") + b"\0"),
        )

        self.symbols["printf"] = printf

    def Prgm(self, statements):
        for statement in statements:
            self.visit(statement)

        self.builder.ret(ir.Constant(ir.IntType(32), 0))

        return self.module

    def Prnt(self, expression):
        printf = self.symbols["printf"]
        format = self.builder.bitcast(
            self.module.get_global("format"), ir.PointerType(ir.IntType(8))
        )
        return self.builder.call(printf, [format, self.visit(expression)])

    def Addn(self, left, right, type):
        return self.builder.add(self.visit(left), self.visit(right))

    def Subn(self, left, right, type):
        return self.builder.sub(self.visit(left), self.visit(right))

    def Muln(self, left, right, type):
        return self.builder.mul(self.visit(left), self.visit(right))

    def Divn(self, left, right, type):
        return self.builder.sdiv(self.visit(left), self.visit(right))

    def Numb(self, value, type):
        return ir.Constant(ir.IntType(32), value)

    def Idnt(self, name, type):
        address = self.symbols[name]
        return self.builder.load(address)

    def Asgn(self, identifier, expression):
        address = self.builder.alloca(ir.IntType(32), name=identifier)
        self.symbols[identifier] = address
        self.builder.store(self.visit(expression), address)
