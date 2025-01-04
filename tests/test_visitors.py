from collections import defaultdict

from cinder.ast import Addn, Numb, Subn, _Expression
from cinder.visitors import Interpreter, Visitor


def test_visitor():
    ast = Addn(Subn(Numb(2), Numb(1)), Numb(3))
    calls = defaultdict(int)
    expected = {"Add": 1, "Sub": 1, "Num": 3}

    class TestVisitor(Visitor):
        def Addn(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Add"] += 1

        def Subn(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Sub"] += 1

        def Numb(self, num):
            assert isinstance(num, int)
            calls["Num"] += 1

    TestVisitor().visit(ast)
    assert calls == expected


def test_interpreter():
    ast = Addn(Subn(Numb(2), Numb(1)), Numb(3))
    calls = defaultdict(int)
    expected = {"Add": 1, "Sub": 1, "Num": 2}

    class TestInterpreter(Interpreter):
        def Addn(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Add"] += 1
            self.visit(left)
            self.visit(right)

        def Subn(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Sub"] += 1
            self.visit(right)

        def Numb(self, num):
            assert isinstance(num, int)
            calls["Num"] += 1

    TestInterpreter().visit(ast)
    assert calls == expected
