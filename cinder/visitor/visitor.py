from cinder.ast.node import _Node


class Visitor:
    def __init__(self):
        self.current = None

    def visit(self, node):
        if isinstance(node, list):
            for element in node:
                self.visit(element)
        elif isinstance(node, _Node):
            children = vars(node).values()
            for child in children:
                self.visit(child)

            self.current = node
            classname = type(node).__name__
            getattr(self, classname, self.__default__)(*children)

    def __default__(self, *args):
        pass
