from dataclasses import dataclass
from typing import List

from cinder.ast import AsList, _Expression, _Node
from cinder.ast.types import Type, Void


@dataclass(unsafe_hash=True)
class _Statement(_Node):
    pass


@dataclass(unsafe_hash=True)
class Print(_Statement):
    expression: _Expression


@dataclass(unsafe_hash=True)
class Assign(_Statement):
    identifier: str
    expression: _Expression

    def __init__(self, identifier, type, expression):
        self.identifier = identifier.name
        self.type = type
        self.expression = expression

    def __str__(self):
        return f"Assign ({self.identifier}: {self.type})"


@dataclass(unsafe_hash=True)
class Block(_Statement, AsList):
    statements: List[_Statement]

    def __str__(self):
        return f"Block ({len(self.statements)})"


@dataclass(unsafe_hash=True)
class IfElse(_Statement, AsList):
    expressions: List[_Expression]
    blocks: List[Block]
    otherwise: Block

    def __init__(self, args):
        self.expressions = []
        self.blocks = []

        while len(args) >= 2:
            self.expressions.append(args.pop(0))
            self.blocks.append(args.pop(0))

        self.otherwise = args.pop() if args else None

    def __str__(self):
        return "If" if self.otherwise is None else "If-Else"


@dataclass(unsafe_hash=True)
class Parameter(_Node):
    name: str
    type: Type

    def __init__(self, identifier, type):
        self.name = identifier.name
        self.type = type


@dataclass(unsafe_hash=True)
class Function(_Node, AsList):
    name: str
    parameters: List[Parameter]
    return_type: Type
    body: Block

    def __init__(self, args):
        self.name = args[0].name
        self.parameters = args[1:-2]
        self.return_type = Void() if args[-2] is None else args[-2]
        self.body = args[-1]


@dataclass(unsafe_hash=True)
class Return(_Statement):
    expression: _Expression
