import sys

from lark import Transformer, ast_utils, v_args


class AstTransformer(Transformer):
    def NUMBER(self, number):
        return int(number)

    @v_args(inline=True)
    def start(self, program):
        return program


module = sys.modules[__name__]
transformer = ast_utils.create_transformer(module, AstTransformer())
