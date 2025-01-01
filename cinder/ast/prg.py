from dataclasses import dataclass

from llvmlite import ir

from cinder.ast.node import _Expression, _Node


@dataclass
class Prg(_Node):
    expression: _Expression

    def compile(self):
        module = ir.Module()
        entry = ir.Function(module, ir.FunctionType(ir.IntType(32), []), "main")
        block = entry.append_basic_block()
        builder = ir.IRBuilder(block)
        builder.ret(self.expression.compile(builder))

        return module
