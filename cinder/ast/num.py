from dataclasses import dataclass

from llvmlite import ir

from cinder.ast.node import _Expression


@dataclass
class Num(_Expression):
    value: int

    def __init__(self, number):
        self.value = int(number)

    def compile(self, module=None, builder=None, symbols=None):
        return ir.Constant(ir.IntType(32), self.value)
