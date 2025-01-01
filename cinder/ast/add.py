from dataclasses import dataclass

from cinder.ast.node import _Expression


@dataclass
class Add(_Expression):
    left: _Expression
    right: _Expression

    def compile(self, builder):
        left = self.left.compile(builder)
        right = self.right.compile(builder)
        return builder.add(left, right)
