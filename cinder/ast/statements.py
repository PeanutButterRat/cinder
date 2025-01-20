from dataclasses import dataclass
from typing import List

from cinder.ast import AsList, _Expression, _Node
from cinder.ast.types import Type, Void


@dataclass
class _Statement(_Node):
    pass


@dataclass
class Print(_Statement):
    expression: _Expression


@dataclass
class Assign(_Statement):
    identifier: str
    expression: _Expression

    def __init__(self, identifier, type, expression):
        self.identifier = identifier.name
        self.type = type
        self.expression = expression

    def __str__(self):
        return f"Assign ({self.identifier}: {self.type})"


@dataclass
class Block(_Statement, AsList):
    statements: List[_Statement]

    def __str__(self):
        return f"Block ({len(self.statements)})"


@dataclass
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


@dataclass
class Function(_Node):
    name: str
    return_type: Type
    body: Block

    def __init__(self, identifier, return_type, body):
        self.name = identifier.name
        self.return_type = Void() if return_type is None else return_type
        self.body = body


@dataclass
class Return(_Statement):
    expresssion: _Expression
