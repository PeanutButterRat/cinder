from dataclasses import dataclass

from cinder.ast.node import _Expression, _Statement


@dataclass
class Prt(_Statement):
    expression: _Expression
