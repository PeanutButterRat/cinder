import subprocess

import pytest

from cinder.cli import compile, parse


@pytest.mark.parametrize(
    "source",
    [
        "let a: i32 = (1 + 2) * 2; let b: i32 = a + 1 * 2;",
        "let foo: i32 = 12; let bar: i32 = foo / 2 + 1; let baz: i32 = foo + bar;",
        "let foo: i32 = 12; let bar: i32 = foo / 2 + 1; print foo + bar;",
    ],
)
def test_compilation(source):
    ast = parse(source)
    compile(ast)
    completed = subprocess.run(["build/output.exe"])

    assert completed.returncode == 0
