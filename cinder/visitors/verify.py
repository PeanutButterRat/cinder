from cinder.ast import _Node
from cinder.symbols import Symbols
from cinder.visitors.visitor import Visitor


class ASTVerifier(Visitor):
    def __init__(self):
        super().__init__()
        self.symbols = Symbols()

    def Asgn(self, identifier, expression):
        self.symbols[identifier] = expression.type

    def Addn(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in addition operation ({left.type}, {right.type})"
        self.current.type = left.type

    def Subn(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in subtraction operation ({left.type}, {right.type})"
        self.current.type = left.type

    def Muln(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in multiplication operation ({left.type}, {right.type})"
        self.current.type = left.type

    def Divn(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in division operation ({left.type}, {right.type})"
        self.current.type = left.type

    def Numb(self, number):
        self.current.type = "i32"

    def Idnt(self, name):
        assert name in self.symbols, f"undefined identifier ({name})"
        self.current.type = self.symbols[name]
