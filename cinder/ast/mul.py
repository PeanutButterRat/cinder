from dataclasses import dataclass

from cinder.ast.node import _Expression


@dataclass
class Mul(_Expression):
    left: _Expression
    right: _Expression
