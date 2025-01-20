import subprocess

import pytest

from cinder.cli import compile, parse


@pytest.mark.parametrize(
    "source, stdout",
    [
        [
            """
            fn main() -> i32 {
                let a: i32 = test() + test();
                print a;
                return 0;
            }

            fn test() -> i32 {
                return 1;
            }
            """,
            "2",
        ],
    ],
)
def test_compilation(source, stdout):
    ast, globals = parse(source)
    compile(ast, globals)

    process = subprocess.run(["build/output.exe"], capture_output=True, text=True)

    assert process.returncode == 0
    assert process.stdout.strip() == stdout
