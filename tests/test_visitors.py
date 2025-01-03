from collections import defaultdict

from cinder.ast import Add, Num, Sub, _Expression
from cinder.visitors import Interpreter, Visitor


def test_visitor():
    ast = Add(Sub(Num(2), Num(1)), Num(3))
    calls = defaultdict(int)
    expected = {"Add": 1, "Sub": 1, "Num": 3}

    class TestVisitor(Visitor):
        def Add(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Add"] += 1

        def Sub(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Sub"] += 1

        def Num(self, num):
            assert isinstance(num, int)
            calls["Num"] += 1

    TestVisitor().visit(ast)
    assert calls == expected


def test_interpreter():
    ast = Add(Sub(Num(2), Num(1)), Num(3))
    calls = defaultdict(int)
    expected = {"Add": 1, "Sub": 1, "Num": 2}

    class TestInterpreter(Interpreter):
        def Add(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Add"] += 1
            self.visit(left)
            self.visit(right)

        def Sub(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Sub"] += 1
            self.visit(right)

        def Num(self, num):
            assert isinstance(num, int)
            calls["Num"] += 1

    TestInterpreter().visit(ast)
    assert calls == expected
