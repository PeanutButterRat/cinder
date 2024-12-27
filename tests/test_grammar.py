import pytest
from lark import Lark

from cinder import GRAMMAR


@pytest.mark.parametrize(
    "rule, valid, invalid",
    (
        (
            "expression",
            ["5 + 2 * (1 / 5)", "((((2)) + 3))/5", "1 * (2) + 3 / (5)"],
            ["5 + + 2", "(((2)) + 3))", "(2 / (3 + 5)"],
        ),
    ),
)
def test_grammar_rule(rule, valid, invalid):
    parser = Lark(GRAMMAR, start=rule)

    for string in valid:
        assert parser.parse(string) is not None

    for string in invalid:
        with pytest.raises(Exception):
            parser.parse(string)
