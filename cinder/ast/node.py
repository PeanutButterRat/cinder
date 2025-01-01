from lark.ast_utils import Ast
from llvmlite import ir

INDENT = "  "


class _Node(Ast):
    def pretty(self, indent=""):
        string = indent + type(self).__name__
        indentation = indent + INDENT

        for attribute in vars(self).values():
            if isinstance(attribute, _Node):
                string += "\n" + attribute.pretty(indentation)
            else:
                string += "\n" + indentation + str(attribute)

        return string

    def verify(self):
        pass

    def compile(self):
        pass


class _Expression(_Node):
    pass
