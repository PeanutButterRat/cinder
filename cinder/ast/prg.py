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

        for statement in self.statements:
            last = statement.compile(builder, Symbols())

        builder.ret(builder.load(last))

        return module
