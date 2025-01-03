from cinder.ast import _Node
from cinder.symbols import Symbols
from cinder.visitors.visitor import Visitor


class ASTVerifier(Visitor):
    def __init__(self):
        super().__init__()
        self.symbols = Symbols()

    def Asn(self, identifier, expression):
        self.symbols[identifier] = expression.type

    def Add(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in addition operation ({left.type}, {right.type})"
        self.current.type = left.type

    def Sub(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in subtraction operation ({left.type}, {right.type})"
        self.current.type = left.type

    def Mul(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in multiplication operation ({left.type}, {right.type})"
        self.current.type = left.type

    def Div(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in division operation ({left.type}, {right.type})"
        self.current.type = left.type

    def Num(self, number):
        self.current.type = "i32"

    def Idn(self, name):
        assert name in self.symbols, f"undefined identifier ({name})"
        self.current.type = self.symbols[name]
