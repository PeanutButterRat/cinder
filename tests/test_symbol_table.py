import pytest

from cinder.symbols import Symbols


def test_symbol_table_scope():
    symbols = Symbols().push().push().pop().pop()

    symbols["a"] = "somedata"
    symbols["b"] = "samedata"
    assert symbols["a"] == "somedata"
    assert symbols["b"] == "samedata"

    symbols = symbols.push()
    symbols["a"] = "otherdata"

    assert symbols["a"] == "otherdata"
    assert symbols["b"] == "samedata"

    symbols = symbols.pop()

    assert symbols["a"] == "somedata"
    assert symbols["b"] == "samedata"


def test_symbol_table_exceptions():
    symbols = Symbols()

    with pytest.raises(Exception):
        symbols["undefined"]

    with pytest.raises(Exception):
        symbols.push().pop().pop()
