import sys

from lark import Transformer, ast_utils, v_args

from cinder.ast.add import Add
from cinder.ast.div import Div
from cinder.ast.mul import Mul
from cinder.ast.prg import Prg
from cinder.ast.sub import Sub


class AstTransformer(Transformer):
    def NUMBER(self, number):
        return int(number)


module = sys.modules[__name__]
transformer = ast_utils.create_transformer(module, AstTransformer())
