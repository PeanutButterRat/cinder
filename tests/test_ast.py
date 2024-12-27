import pytest
from lark import Lark

from cinder import GRAMMAR
from cinder.ast import transformer


@pytest.mark.parametrize(
    "rule, strings",
    (
        (
            "expression",
            ["5 + 2 * (1 / 5)", "((((2)) + 3))/5", "1 * (2) + 3 / (5)"],
        ),
    ),
)
def test_grammar_rule(rule, strings):
    parser = Lark(GRAMMAR, start=rule)

    for string in strings:
        cst = parser.parse(string)
        ast = transformer.transform(cst)
        assert ast is not None
