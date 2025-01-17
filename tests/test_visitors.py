from collections import defaultdict

from cinder.ast import Addition, Number, Subtraction, _Expression
from cinder.visitors import Interpreter, Visitor


def test_visitor():
    ast = Addition(Subtraction(Number(2), Number(1)), Number(3))
    calls = defaultdict(int)
    expected = {"Add": 1, "Sub": 1, "Num": 3}

    class TestVisitor(Visitor):
        def Addition(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Add"] += 1

        def Subtraction(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Sub"] += 1

        def Number(self, num):
            assert isinstance(num, int)
            calls["Num"] += 1

    TestVisitor().visit(ast)
    assert calls == expected


def test_interpreter():
    ast = Addition(Subtraction(Number(2), Number(1)), Number(3))
    calls = defaultdict(int)
    expected = {"Add": 1, "Sub": 1, "Num": 2}

    class TestInterpreter(Interpreter):
        def Addition(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Add"] += 1
            self.visit(left)
            self.visit(right)

        def Subtraction(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Sub"] += 1
            self.visit(right)

        def Number(self, num):
            assert isinstance(num, int)
            calls["Num"] += 1

    TestInterpreter().visit(ast)
    assert calls == expected
