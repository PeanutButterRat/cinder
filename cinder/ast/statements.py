from dataclasses import dataclass
from typing import List

from cinder.ast import AsList, _Node
from cinder.ast.expressions import _Expression


@dataclass
class _Statement(_Node):
    pass


@dataclass
class Prnt(_Statement):
    expression: _Expression


@dataclass
class Asgn(_Statement):
    identifier: str
    expression: _Expression

    def __init__(self, identifier, type, expression):
        self.identifier = identifier.name
        self.type = type
        self.expression = expression


@dataclass
class Blck(_Statement, AsList):
    statements: List[_Statement]


@dataclass
class Ifel(_Statement, AsList):
    expressions: List[_Expression]
    blocks: List[Blck]
    otherwise: Blck

    def __init__(self, args):
        self.expressions = []
        self.blocks = []

        while len(args) >= 2:
            self.expressions.append(args.pop(0))
            self.blocks.append(args.pop(0))

        self.otherwise = args.pop() if args else None
