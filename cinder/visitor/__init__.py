from cinder.ast.node import _Node


class Visitor:
    def visit(self, node):
        if isinstance(node, _Node):
            children = vars(node).values()
            for child in children:
                self.visit(child)

            classname = type(node).__name__
            getattr(self, classname, self.__default__)(*children)

    def __default__(self, node):
        pass
