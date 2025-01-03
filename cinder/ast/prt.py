from dataclasses import dataclass

from cinder.ast.expressions import _Expression
from cinder.ast.node import _Statement


@dataclass
class Prt(_Statement):
    expression: _Expression
