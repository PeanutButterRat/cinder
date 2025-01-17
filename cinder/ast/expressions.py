from dataclasses import dataclass, field

from cinder.ast.node import _Node


@dataclass
class _Expression(_Node):
    type: str = field(default=None, init=False)


@dataclass
class Addn(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "+"


@dataclass
class Subn(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "-"


@dataclass
class Muln(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "*"


@dataclass
class Divn(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "/"


@dataclass
class Numb(_Expression):
    value: int

    def __init__(self, number):
        self.value = int(number)

    def __str__(self):
        return str(self.value)


@dataclass
class Bool(_Expression):
    value: bool

    def __init__(self, bool):
        self.value = bool == "true"

    def __str__(self):
        return str(self.value)


@dataclass
class Idnt(_Node):
    name: str

    def __init__(self, name):
        self.name = name.value


@dataclass
class Grth(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return ">"


@dataclass
class Greq(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return ">="


@dataclass
class Lsth(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "<"


@dataclass
class Lseq(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "<="


@dataclass
class Nteq(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "!="


@dataclass
class Equl(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "=="


@dataclass
class Andx(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "And"


@dataclass
class Orxp(_Expression):
    left: _Expression
    right: _Expression

    def __str__(self):
        return "Or"


@dataclass
class Notx(_Expression):
    expression: _Expression

    def __str__(self):
        return "Not"
