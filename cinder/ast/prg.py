from dataclasses import dataclass
from typing import List

from cinder.ast.node import AsList, _Node, _Statement


@dataclass
class Prg(_Node, AsList):
    statements: List[_Statement]
