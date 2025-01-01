from dataclasses import dataclass

from llvmlite import ir

from cinder.ast.node import _Expression, _Statement


@dataclass
class Asn(_Statement):
    identifier: str
    expression: _Expression

    def __init__(self, identifier, expression):
        self.identifier = identifier.name
        self.expression = expression

    def compile(self, builder=None, symbols=None):
        address = builder.alloca(ir.IntType(32), name=self.identifier)
        builder.store(self.expression.compile(builder), address)
        return address
