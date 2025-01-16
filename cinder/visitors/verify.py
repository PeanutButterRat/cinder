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

    def Bool(self, boolean):
        self.current.type = bool()

    def Idnt(self, name):
        assert name in self.symbols, f"undefined identifier ({name})"
        self.current.type = self.symbols[name]

    def comparison(self, left, right):
        assert isinstance(
            left.type, i32
        ), f"left side of comparison is not integer expession ({left.type})"
        assert isinstance(
            right.type, i32
        ), f"right side of comparison is not integer expession ({right.type})"
        self.current.type = bool()

    Grth = comparison
    Greq = comparison
    Lsth = comparison
    Lseq = comparison
    Nteq = comparison
    Equl = comparison

    def Andx(self, left, right):
        assert isinstance(
            left.type, bool
        ), f"left side of boolean and is not boolean expressions ({left.type})"
        assert isinstance(
            right.type, bool
        ), f"right side of boolean and is not boolean expressions ({right.type})"
        self.current.type = bool()

    def Orxp(self, left, right):
        assert isinstance(
            left.type, bool
        ), f"left side of boolean or is not boolean expressions ({left.type})"
        assert isinstance(
            right.type, bool
        ), f"right side of boolean or is not boolean expressions ({right.type})"
        self.current.type = bool()

    def Notx(self, expression):
        assert isinstance(
            expression.type, bool
        ), f"expression for boolean not is not boolean expressions ({expression.type})"
        self.current.type = bool()
