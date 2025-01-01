from dataclasses import dataclass

from llvmlite import ir

from cinder.ast.node import _Node


@dataclass
class Idn(_Node):
    name: str

    def __init__(self, name):
        self.name = name.value

    def compile(self, builder=None, symbols=None):
        address = symbols[self.name]
        return builder.load(address)
