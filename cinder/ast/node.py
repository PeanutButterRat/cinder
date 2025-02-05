from dataclasses import dataclass

import treelib
from lark.ast_utils import Ast


@dataclass(unsafe_hash=True)
class _Node(Ast):
    def pretty(self, tree=treelib.Tree()):
        def helper(ast, parent=None):
            tree.create_node(str(ast), id(ast), parent)
            children = []

            for attribute in vars(ast).values():
                if isinstance(attribute, _Node):
                    children.append(attribute)
                elif isinstance(attribute, list):
                    children.extend(
                        [attr for attr in attribute if isinstance(attr, _Node)]
                    )

            for child in children:
                helper(child, id(ast))

            return id(ast)

        helper(self)

        return tree

    def __str__(self):
        return type(self).__name__
