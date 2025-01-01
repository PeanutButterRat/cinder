from dataclasses import dataclass

from cinder.ast.node import _Expression


@dataclass
class Add(_Expression):
    left: _Expression
    right: _Expression

    def compile(self, builder=None, symbols=None):
        left = self.left.compile(builder, symbols)
        right = self.right.compile(builder, symbols)
        return builder.add(left, right)
