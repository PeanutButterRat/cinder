from dataclasses import dataclass

from cinder.ast.expressions import _Expression
from cinder.ast.node import _Node


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

    def __init__(self, identifier, expression):
        self.identifier = identifier.name
        self.expression = expression
