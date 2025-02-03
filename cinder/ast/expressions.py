from dataclasses import dataclass
from typing import List

from lark.ast_utils import AsList

from cinder.ast.node import _Node


@dataclass(unsafe_hash=True)
class _Expression(_Node):
    pass


@dataclass(unsafe_hash=True)
class Addition(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "+"


@dataclass(unsafe_hash=True)
class Subtraction(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "-"


@dataclass(unsafe_hash=True)
class Multiplication(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "*"


@dataclass(unsafe_hash=True)
class Division(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "/"


@dataclass(unsafe_hash=True)
class Number(_Expression):
    value: int

    def __init__(self, number):
        self.value = int(number)

    def __str__(self):
        return str(self.value)


@dataclass(unsafe_hash=True)
class Boolean(_Expression):
    value: bool

    def __init__(self, bool):
        self.value = bool == "true"

    def __str__(self):
        return str(self.value)


@dataclass(unsafe_hash=True)
class Identifier(_Node):
    name: str

    def __init__(self, name):
        self.name = name.value


@dataclass(unsafe_hash=True)
class GreaterThan(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return ">"


@dataclass(unsafe_hash=True)
class GreaterEqual(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return ">="


@dataclass(unsafe_hash=True)
class LessThan(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "<"


@dataclass(unsafe_hash=True)
class LessEqual(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "<="


@dataclass(unsafe_hash=True)
class NotEqual(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "!="


@dataclass(unsafe_hash=True)
class Equal(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "=="


@dataclass(unsafe_hash=True)
class And(_Expression):
    left: _Expression
    right: _Expression


@dataclass(unsafe_hash=True)
class Or(_Expression):
    left: _Expression
    right: _Expression


@dataclass(unsafe_hash=True)
class Not(_Expression):
    expression: _Expression


class Call(_Expression, AsList):
    name: str
    expressions: List[_Expression]

    def __init__(self, args):
        self.name = args[0].name
        self.expressions = args[1:]
