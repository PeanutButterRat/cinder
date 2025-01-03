from llvmlite import ir

from cinder.ast import _Node
from cinder.symbols import Symbols
from cinder.visitors.visitor import Visitor


class ASTCompiler(Visitor):
    def __init__(self):
        super().__init__()
        self.symbols = Symbols()
        self.module = ir.Module()
        self.instructions = {}

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

    def visit(self, node):
        super().visit(node)
        return self.module

    def Prg(self, statements):
        self.builder.ret(ir.Constant(ir.IntType(32), 0))

    def Prt(self, expression):
        printf = self.symbols["printf"]
        format = self.builder.bitcast(
            self.module.get_global("format"), ir.PointerType(ir.IntType(8))
        )
        self.builder.call(printf, [format, self.instructions[id(expression)]])

    def Add(self, left, right, type):
        instruction = self.builder.add(
            self.instructions[id(left)], self.instructions[id(right)]
        )
        self.instructions[id(self.current)] = instruction

    def Sub(self, left, right, type):
        instruction = self.builder.sub(
            self.instructions[id(left)], self.instructions[id(right)]
        )
        self.instructions[id(self.current)] = instruction

    def Mul(self, left, right, type):
        instruction = self.builder.mul(
            self.instructions[id(left)], self.instructions[id(right)]
        )
        self.instructions[id(self.current)] = instruction

    def Div(self, left, right, type):
        instruction = self.builder.sdiv(
            self.instructions[id(left)], self.instructions[id(right)]
        )
        self.instructions[id(self.current)] = instruction

    def Num(self, value, type):
        self.instructions[id(self.current)] = ir.Constant(ir.IntType(32), value)

    def Idn(self, name, type):
        address = self.symbols[name]
        self.instructions[id(self.current)] = self.builder.load(address)

    def Asn(self, identifier, expression):
        address = self.builder.alloca(ir.IntType(32), name=identifier)
        self.builder.store(self.instructions[id(expression)], address)
        self.symbols[identifier] = address
