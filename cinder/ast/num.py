from dataclasses import dataclass

from cinder.ast.node import _Expression


@dataclass
class Num(_Expression):
    value: int

    def __init__(self, number):
        self.value = int(number)
