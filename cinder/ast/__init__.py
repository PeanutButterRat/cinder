import sys

from lark import Transformer, ast_utils

from cinder.ast.add import Add
from cinder.ast.asn import Asn
from cinder.ast.div import Div
from cinder.ast.idn import Idn
from cinder.ast.mul import Mul
from cinder.ast.num import Num
from cinder.ast.prg import Prg
from cinder.ast.sub import Sub


class AstTransformer(Transformer):
    def IDENTIFIER(self, name):
        return Idn(name)


module = sys.modules[__name__]
transformer = ast_utils.create_transformer(module, AstTransformer())
