import sys
from typing import List

from lark import Transformer
from lark.ast_utils import AsList, create_transformer

from cinder.ast.expressions import *
from cinder.ast.expressions import _Expression
from cinder.ast.node import _Node
from cinder.ast.statements import *
from cinder.ast.statements import _Statement


class AstTransformer(Transformer):
    def IDENTIFIER(self, name):
        return Idn(name)


@dataclass
class Prg(_Node, AsList):
    statements: List[_Statement]


module = sys.modules[__name__]
transformer = create_transformer(module, AstTransformer())
