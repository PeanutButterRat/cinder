from cinder.ast import _Node
from cinder.ast.types import *
from cinder.symbols import Symbols
from cinder.visitor.visitor import Interpreter, Visitor


class ExpressionVerifier(Visitor):
    def __init__(self, symbols):
        super().__init__()
        self.symbols = symbols
        self.expressions = {}

    def arithmetic(operator):
        def verification(self, left, right):
            assert (
                self.expressions[left] == self.expressions[right]
            ), f"mismatched types in arithmetic expression ({self.expressions[left]} {operator} {self.expressions[right]})"
            self.expressions[self.current] = self.expressions[left]

        return verification

    Addition = arithmetic("+")
    Subtraction = arithmetic("-")
    Multiplication = arithmetic("*")
    Division = arithmetic("/")

    def Number(self, number):
        self.expressions[self.current] = Integer(32)

    def Boolean(self, boolean):
        self.expressions[self.current] = Boolean()

    def Identifier(self, name):
        assert name in self.symbols, f"undefined identifier ({name})"
        self.expressions[self.current] = self.symbols[name]

    def comparison(operator):
        def verification(self, left, right):
            assert self.expressions[left] == Integer(
                32
            ), f"left side of comparison ({operator}) is not an integer expession ({self.expressions[left]})"
            assert self.expressions[right] == Integer(
                32
            ), f"right side of comparison ({operator}) is not an integer expession ({self.expressions[right]})"
            self.expressions[self.current] = Boolean()

        return verification

    GreaterThan = comparison(">")
    GreaterEqual = comparison(">=")
    LessThan = comparison("<")
    LessEqual = comparison("<=")
    NotEqual = comparison("!=")
    Equal = comparison("==")

    def logical_expression(operator):
        def verification(self, left, right):
            assert (
                self.expressions[left] == Boolean()
            ), f"left side of boolean expression ({operator}) is not boolean expressions ({self.expressions[left]})"
            assert (
                self.expressions[right] == Boolean()
            ), f"right side of boolean expression ({operator}) is not boolean expressions ({self.expressions[right]})"
            self.expressions[self.current] = Boolean()

        return verification

    And = logical_expression("and")
    Or = logical_expression("or")

    def Not(self, expression):
        assert (
            self.expressions[expression] == Boolean()
        ), f"expression for boolean not is not boolean expressions ({self.expressions[expression]})"
        self.expressions[self.current] = Boolean()

    def Call(self, name):
        assert name in self.symbols, f"function is undefined ({name})"
        assert isinstance(
            self.symbols[name], Function
        ), f"identifier is not callable ({name})"
        self.expressions[self.current] = self.symbols[name].return_type


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
                self.symbols[name] = Function(function.return_type)

        for function in functions:
            self.visit(function)

        return self.symbols

    def Function(self, name, return_type, body):
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
                self.verifier.expressions[condition] == Boolean()
            ), "condition for if-else statement is not boolean expression"

        for block in blocks:
            self.visit(block)

        self.visit(otherwise)

    def Assign(self, identifier, type, expression):
        self.verifier.visit(expression)
        assert (
            type == self.verifier.expressions[expression]
        ), f"mismatched types in assignment ({type}, {self.verifier.expressions[expression]})"
        self.symbols[identifier] = self.verifier.expressions[expression]

    def Print(self, expression):
        self.verifier.visit(expression)

    def Call(self, name):
        assert name in self.symbols, f"function is undefined ({name})"
        assert isinstance(
            self.symbols[name], Function
        ), f"identifier is not callable ({name})"

    def Return(self, expression):
        self.verifier.visit(expression)
