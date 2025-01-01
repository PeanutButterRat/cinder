import sys

from lark import Transformer, ast_utils, v_args

from cinder.ast.add import Add
from cinder.ast.div import Div
from cinder.ast.mul import Mul
from cinder.ast.num import Num
from cinder.ast.prg import Prg
from cinder.ast.sub import Sub


class AstTransformer(Transformer):
    pass


module = sys.modules[__name__]
transformer = ast_utils.create_transformer(module, AstTransformer())
