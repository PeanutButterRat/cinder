from cinder.ast import _Node
from cinder.ast.type import *
from cinder.symbols import Symbols
from cinder.visitors.visitor import Visitor


class ASTVerifier(Visitor):
    def __init__(self):
        super().__init__()
        self.symbols = Symbols()

    def Assign(self, identifier, type, expression):
        assert (
            type == expression.type
        ), f"mismatched types in assignment ({type}, {expression.type})"
        self.symbols[identifier] = expression.type

    def Addition(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in addition expression ({left.type}, {right.type})"
        self.current.type = left.type

    def Subtraction(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in subtraction expression ({left.type}, {right.type})"
        self.current.type = left.type

    def Multiplication(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in multiplication expression ({left.type}, {right.type})"
        self.current.type = left.type

    def Division(self, left, right):
        assert (
            left.type == right.type
        ), f"mismatched types in division expression ({left.type}, {right.type})"
        self.current.type = left.type

    def Number(self, number):
        self.current.type = i32()

    def Boolean(self, boolean):
        self.current.type = bool()

    def Identifier(self, name):
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

    GreaterThan = comparison
    GreaterEqual = comparison
    LessThan = comparison
    LessEqual = comparison
    NotEqual = comparison
    Equal = comparison

    def And(self, left, right):
        assert isinstance(
            left.type, bool
        ), f"left side of boolean and is not boolean expressions ({left.type})"
        assert isinstance(
            right.type, bool
        ), f"right side of boolean and is not boolean expressions ({right.type})"
        self.current.type = bool()

    def Or(self, left, right):
        assert isinstance(
            left.type, bool
        ), f"left side of boolean or is not boolean expressions ({left.type})"
        assert isinstance(
            right.type, bool
        ), f"right side of boolean or is not boolean expressions ({right.type})"
        self.current.type = bool()

    def Not(self, expression):
        assert isinstance(
            expression.type, bool
        ), f"expression for boolean not is not boolean expressions ({expression.type})"
        self.current.type = bool()

    def Function(self, name, body):
        pass

    def Call(self, name):
        pass
