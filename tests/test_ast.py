import pytest
from lark import Lark

from cinder import GRAMMAR
from cinder.ast import transformer
from cinder.ast.node import _Node
from cinder.visitors.verify import TreeVerifier


@pytest.mark.parametrize(
    "rule, strings",
    [
        [
            "arithmetic",
            ["5 + 2 * (1 / 5)", "((((2)) + 3))/5", "1 * (2) + 3 / (5)"],
        ],
        [
            "statement",
            [
                "if true { print 1; } elif false { print 2; } else { print 3; }",
                "let a: bool = true or false and 1 + 2 * 3 == 6 and false;",
            ],
        ],
    ],
)
def test_grammar_rule(rule, strings):
    parser = Lark(GRAMMAR, start=rule)

    for string in strings:
        cst = parser.parse(string)
        ast = transformer.transform(cst)
        TreeVerifier().visit(ast)
        assert isinstance(ast, _Node)
