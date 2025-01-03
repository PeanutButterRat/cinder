import sys

from lark import Transformer, ast_utils

from cinder.ast.expressions import *
from cinder.ast.expressions import _Expression
from cinder.ast.prg import Prg
from cinder.ast.statements import *
from cinder.ast.statements import _Statement


class AstTransformer(Transformer):
    def IDENTIFIER(self, name):
        return Idn(name)


module = sys.modules[__name__]
transformer = ast_utils.create_transformer(module, AstTransformer())
