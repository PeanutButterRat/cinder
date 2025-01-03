from dataclasses import dataclass, field

from cinder.ast.node import _Node


@dataclass
class _Expression(_Node):
    type: str = field(default=None, init=False)


@dataclass
class Add(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Sub(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Mul(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Div(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Num(_Expression):
    value: int

    def __init__(self, number):
        self.value = int(number)


@dataclass
class Idn(_Node):
    name: str

    def __init__(self, name):
        self.name = name.value
