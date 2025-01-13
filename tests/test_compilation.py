import subprocess

import pytest

from cinder.cli import compile, parse


@pytest.mark.parametrize(
    "source",
    [
        "let a = (1 + 2) * 2; let b = a + 1 * 2;",
        "let foo = 12; let bar = foo / 2 + 1; let baz = foo + bar;",
        "let foo = 12; let bar = foo / 2 + 1; print foo + bar;",
    ],
)
def test_compilation(source):
    ast = parse(source)
    compile(ast)
    completed = subprocess.run(["build/output.exe"])

    assert completed.returncode == 0
