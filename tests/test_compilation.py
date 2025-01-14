import subprocess

import pytest

from cinder.cli import compile, parse


@pytest.mark.parametrize(
    "source, stdout",
    [
        ("let foo: i32 = 12; let bar: i32 = foo / 2 + 1; print foo + bar;", "19"),
        ("let True: bool = 1 + 2 > 2; if True { print 1; } else { print 0; }", "1"),
        ("if (1 * 2 + 1) == 3 { print 100; }", "100"),
    ],
)
def test_compilation(source, stdout):
    ast = parse(source)
    compile(ast)

    process = subprocess.run(["build/output.exe"], capture_output=True, text=True)

    assert process.returncode == 0
    assert process.stdout.strip() == stdout
