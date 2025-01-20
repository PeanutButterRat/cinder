from cinder.ast import _Node
from cinder.ast.types import *
from cinder.symbols import Symbols
from cinder.visitors.visitor import Interpreter, Visitor


class ExpressionVerifier(Visitor):
    def __init__(self, symbols):
        super().__init__()
        self.symbols = symbols

    def arithmetic(operation):
        def verification(self, left, right):
            assert (
                left.type == right.type
            ), f"mismatched types in {operation} expression ({left.type}, {right.type})"
            self.current.type = left.type

        return verification

    Addition = arithmetic("addition")
    Subtraction = arithmetic("subtraction")
    Multiplication = arithmetic("multiplication")
    Division = arithmetic("division")

    def Number(self, number):
        self.current.type = Integer(32)

    def Boolean(self, boolean):
        self.current.type = Boolean()

    def Identifier(self, name):
        assert name in self.symbols, f"undefined identifier ({name})"
        self.current.type = self.symbols[name]

    def comparison(self, left, right):
        assert left.type == Integer(
            32
        ), f"left side of comparison is not integer expession ({left.type})"
        assert right.type == Integer(
            32
        ), f"right side of comparison is not integer expession ({right.type})"
        self.current.type = Boolean()

    GreaterThan = comparison
    GreaterEqual = comparison
    LessThan = comparison
    LessEqual = comparison
    NotEqual = comparison
    Equal = comparison

    def And(self, left, right):
        assert (
            left.type == Boolean()
        ), f"left side of boolean and is not boolean expressions ({left.type})"
        assert (
            right.type == Boolean()
        ), f"right side of boolean and is not boolean expressions ({right.type})"
        self.current.type = Boolean()

    def Or(self, left, right):
        assert (
            left.type == Boolean()
        ), f"left side of boolean or is not boolean expressions ({left.type})"
        assert (
            right.type == Boolean()
        ), f"right side of boolean or is not boolean expressions ({right.type})"
        self.current.type = Boolean()

    def Not(self, expression):
        assert (
            expression.type == Boolean()
        ), f"expression for boolean not is not boolean expressions ({expression.type})"
        self.current.type = Boolean()

    def Call(self, name):
        pass


class TreeVerifier(Interpreter):
    def __init__(self):
        super().__init__()
        self.symbols = Symbols()
        self.verifier = ExpressionVerifier(self.symbols)

    def Program(self, functions):
        for function in functions:
            name = function.name

            if name in self.symbols:
                raise RuntimeError(f"function previously defined ({name})")
            else:
                self.symbols[name] = Function(Integer(32))

        for function in functions:
            self.visit(function)

        return self.symbols

    def Function(self, name, body):
        self.visit(body)

    def Block(self, statements):
        self.symbols = self.symbols.push()

        for statement in statements:
            self.visit(statement)

        self.symbols = self.symbols.pop()

    def IfElse(self, conditions, blocks, otherwise):
        for condition in conditions:
            self.verifier.visit(condition)
            assert (
                condition.type == Boolean()
            ), "condition for if-else statement is not boolean expression"

        for block in blocks:
            self.visit(block)

        self.visit(otherwise)

    def Assign(self, identifier, type, expression):
        self.verifier.visit(expression)
        assert (
            type == expression.type
        ), f"mismatched types in assignment ({type}, {expression.type})"
        self.symbols[identifier] = expression.type

    def Print(self, expression):
        self.verifier.visit(expression)

    def Call(self, name):
        assert name in self.symbols, f"function is used but is not defined ({name})"
        assert isinstance(
            self.symbols[name], Function
        ), f"identifier is not callable ({name})"
