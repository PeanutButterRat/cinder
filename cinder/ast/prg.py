from dataclasses import dataclass

from cinder.ast.node import _Expression, _Node


@dataclass
class Prg(_Node):
    expression: _Expression
