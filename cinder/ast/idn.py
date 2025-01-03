from dataclasses import dataclass

from cinder.ast.node import _Node


@dataclass
class Idn(_Node):
    name: str

    def __init__(self, name):
        self.name = name.value
