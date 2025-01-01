from dataclasses import dataclass

from cinder.ast.node import _Expression


@dataclass
class Sub(_Expression):
    left: _Expression
    right: _Expression

    def compile(self, builder=None, symbols=None):
        left = self.left.compile(builder)
        right = self.right.compile(builder)
        return builder.sub(left, right)
