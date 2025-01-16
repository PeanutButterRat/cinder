from dataclasses import dataclass

from lark.ast_utils import Ast

INDENT = "  "


@dataclass
class _Node(Ast):
    def pretty(self, indent=""):
        string = indent + type(self).__name__
        indentation = indent + INDENT

        def format(value):
            if isinstance(value, _Node):
                return value.pretty(indentation)
            else:
                return indentation + str(value)

        for attribute in vars(self).values():
            if isinstance(attribute, list):
                for element in attribute:
                    string += "\n" + format(element)
            else:
                string += "\n" + format(attribute)

        return string
