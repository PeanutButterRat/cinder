from cinder.ast import _Node
from cinder.ast.type import *
from cinder.symbols import Symbols
from cinder.visitors.visitor import Visitor


class ASTVerifier(Visitor):
    def __init__(self):
        super().__init__()
        self.symbols = Symbols()

    def Asgn(self, identifier, type, expression):
        assert (
            type == expression.type
        ), f"mismatched types in assignment ({type}, {expression.type})"
        self.symbols[identifier] = expression.type

    def Addn(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in addition expression ({left.type}, {right.type})"
        self.current.type = left.type

    def Subn(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in subtraction expression ({left.type}, {right.type})"
        self.current.type = left.type

    def Muln(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in multiplication expression ({left.type}, {right.type})"
        self.current.type = left.type

    def Divn(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in division expression ({left.type}, {right.type})"
        self.current.type = left.type

    def Numb(self, number):
        self.current.type = i32()

    def Idnt(self, name):
        assert name in self.symbols, f"undefined identifier ({name})"
        self.current.type = self.symbols[name]
