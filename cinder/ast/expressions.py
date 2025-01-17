from dataclasses import dataclass, field

from cinder.ast.node import _Node


@dataclass
class _Expression(_Node):
    type: str = field(default=None, init=False)


@dataclass
class Addition(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "+"


@dataclass
class Subtraction(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "-"


@dataclass
class Multiplication(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "*"


@dataclass
class Division(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "/"


@dataclass
class Number(_Expression):
    value: int

    def __init__(self, number):
        self.value = int(number)

    def __str__(self):
        return str(self.value)


@dataclass
class Boolean(_Expression):
    value: bool

    def __init__(self, bool):
        self.value = bool == "true"

    def __str__(self):
        return str(self.value)


@dataclass
class Identifier(_Node):
    name: str

    def __init__(self, name):
        self.name = name.value


@dataclass
class GreaterThan(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return ">"


@dataclass
class GreaterEqual(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return ">="


@dataclass
class LessThan(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "<"


@dataclass
class LessEqual(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "<="


@dataclass
class NotEqual(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "!="


@dataclass
class Equal(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "=="


@dataclass
class And(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Or(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Not(_Expression):
    expression: _Expression


class Call(_Expression):
    name: str

    def __init__(self, identifier):
        self.name = identifier.name
