from dataclasses import dataclass
from typing import List

from llvmlite import ir

from cinder.ast.node import AsList, _Node, _Statement
from cinder.symbols import Symbols


@dataclass
class Prg(_Node, AsList):
    statements: List[_Statement]

    def compile(self, builder=None, symbols=None):
        module = ir.Module()
        entry = ir.Function(module, ir.FunctionType(ir.IntType(32), []), "main")
        block = entry.append_basic_block()
        builder = ir.IRBuilder(block)
        symbols = Symbols()

        printf = ir.Function(
            module,
            ir.FunctionType(
                ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True
            ),
            name="printf",
        )

        format = ir.GlobalVariable(
            module, ir.ArrayType(ir.IntType(8), count=4), name="format"
        )
        format.global_constant = True
        format.initializer = ir.Constant(
            ir.ArrayType(ir.IntType(8), count=4),
            bytearray("%d\n".encode("utf8") + b"\0"),
        )

        symbols["printf"] = printf

        for statement in self.statements:
            statement.compile(module, builder, symbols)

        builder.ret(ir.Constant(ir.IntType(32), 0))

        return module
