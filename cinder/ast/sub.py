from dataclasses import dataclass

from cinder.ast.node import _Expression


@dataclass
class Sub(_Expression):
    left: _Expression
    right: _Expression

    def compile(self, module=None, builder=None, symbols=None):
        left = self.left.compile(module, builder, symbols)
        right = self.right.compile(module, builder, symbols)
        return builder.sub(left, right)
