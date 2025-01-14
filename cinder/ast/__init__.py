import sys
from typing import List

from lark import Transformer
from lark.ast_utils import AsList, create_transformer

from cinder.ast.expressions import *
from cinder.ast.expressions import _Expression
from cinder.ast.node import _Node
from cinder.ast.statements import *
from cinder.ast.statements import _Statement
from cinder.ast.type import Type


class AstTransformer(Transformer):
    def CNAME(self, name):
        return Idnt(name)

    def TYPE(self, type):
        return Type.from_string(type)


@dataclass
class Prgm(_Node, AsList):
    statements: List[_Statement]


module = sys.modules[__name__]
transformer = create_transformer(module, AstTransformer())
