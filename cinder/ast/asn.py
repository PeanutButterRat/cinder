from dataclasses import dataclass

from cinder.ast.node import _Expression, _Statement


@dataclass
class Asn(_Statement):
    identifier: str
    expression: _Expression

    def __init__(self, identifier, expression):
        self.identifier = identifier.name
        self.expression = expression
