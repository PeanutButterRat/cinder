from dataclasses import dataclass

from cinder.ast.node import _Expression


@dataclass
class Div(_Expression):
    left: _Expression
    right: _Expression

    def compile(self, builder):
        left = self.left.compile(builder)
        right = self.right.compile(builder)
        return builder.sdiv(left, right)
