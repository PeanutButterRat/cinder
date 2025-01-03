from collections import defaultdict

from cinder.ast.add import Add
from cinder.ast.node import _Expression
from cinder.ast.num import Num
from cinder.ast.sub import Sub
from cinder.visitor import Visitor


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
