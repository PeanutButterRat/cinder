from dataclasses import dataclass, field

from lark.ast_utils import AsList, Ast

INDENT = "  "


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


@dataclass
class _Expression(_Node):
    type: str = field(default=None, init=False)


class _Statement(_Node):
    pass
