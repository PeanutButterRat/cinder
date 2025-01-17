import subprocess

import pytest

from cinder.cli import compile, parse


@pytest.mark.parametrize(
    "source, stdout",
    [
        ["fn test() { print 1; } fn main() { test(); test(); }", "1\n1"],
    ],
)
def test_compilation(source, stdout):
    ast, globals = parse(source)
    compile(ast, globals)

    process = subprocess.run(["build/output.exe"], capture_output=True, text=True)

    assert process.returncode == 0
    assert process.stdout.strip() == stdout
