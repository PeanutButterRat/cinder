import subprocess

import pytest

from cinder.cli import compile


@pytest.mark.parametrize(
    "source, output",
    (
        ("let a = (1 + 2) * 2; let b = a + 1 * 2;", 8),
        ("let foo = 12; let bar = foo / 2 + 1; let baz = foo + bar;", 19),
    ),
)
def test_compilation(source, output):
    compile(source)
    completed = subprocess.run(["build/output.exe"])

    assert completed.returncode == output
