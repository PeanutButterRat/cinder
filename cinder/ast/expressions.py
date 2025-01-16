from dataclasses import dataclass, field

from cinder.ast.node import _Node


@dataclass
class _Expression(_Node):
    type: str = field(default=None, init=False)


@dataclass
class Addn(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Subn(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Muln(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Divn(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Numb(_Expression):
    value: int

    def __init__(self, number):
        self.value = int(number)


@dataclass
class Bool(_Expression):
    value: bool

    def __init__(self, bool):
        self.value = bool == "true"


@dataclass
class Idnt(_Node):
    name: str

    def __init__(self, name):
        self.name = name.value


@dataclass
class Grth(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Greq(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Lsth(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Lseq(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Nteq(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Equl(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Andx(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Orxp(_Expression):
    left: _Expression
    right: _Expression


@dataclass
class Notx(_Expression):
    expression: _Expression
