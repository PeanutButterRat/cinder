from collections import defaultdict

from cinder.ast import Addition, Number, Subtraction, _Expression
from cinder.visitor import Interpreter, Visitor


def test_visitor():
    ast = Addition(Subtraction(Number(2), Number(1)), Number(3))
    calls = defaultdict(int)
    call_order = []
    expected_calls = {"Addition": 1, "Subtraction": 1, "Number": 3}

    class TestVisitor(Visitor):
        def Addition(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            call_order.append("Addition")
            calls["Addition"] += 1

        def Subtraction(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            call_order.append("Subtraction")
            calls["Subtraction"] += 1

        def Number(self, num):
            assert isinstance(num, int)
            call_order.append("Number")
            calls["Number"] += 1

    visitor = TestVisitor()
    visitor.visit(ast)
    assert calls == expected_calls
    assert call_order == ["Number", "Number", "Subtraction", "Number", "Addition"]

    calls.clear()
    call_order.clear()

    visitor.visit(ast, top_down=True)
    assert calls == expected_calls
    assert call_order == ["Addition", "Subtraction", "Number", "Number", "Number"]


def test_interpreter():
    ast = Addition(Subtraction(Number(2), Number(1)), Number(3))
    calls = defaultdict(int)
    expected = {"Addition": 1, "Subtraction": 1, "Number": 2}

    class TestInterpreter(Interpreter):
        def Addition(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Addition"] += 1
            self.visit(left)
            self.visit(right)

        def Subtraction(self, left, right):
            assert isinstance(left, _Expression)
            assert isinstance(right, _Expression)
            calls["Subtraction"] += 1
            self.visit(right)

        def Number(self, num):
            assert isinstance(num, int)
            calls["Number"] += 1

    TestInterpreter().visit(ast)
    assert calls == expected
