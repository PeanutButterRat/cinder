import os
import subprocess
from os.path import dirname, join, realpath

import pytest

from cinder.cli import compile, parse

TEST_DIRECTORY = join(dirname(realpath(__file__)), "programs")
FILENAMES = [join(TEST_DIRECTORY, file) for file in os.listdir(TEST_DIRECTORY)]


@pytest.mark.parametrize("filepath", FILENAMES)
def test_compilation(filepath):
    file = open(filepath)
    source = file.readlines()
    stdout = []

    for line in source:
        print(line)
        if line.startswith("//"):
            stdout.append(line.lstrip("//").strip())
        else:
            break

    stdout = "\n".join(stdout)
    source = "".join(source)
    file.close()

    ast, globals = parse(source)
    compile(ast, globals)

    process = subprocess.run(["build/output.exe"], capture_output=True, text=True)

    assert process.returncode == 0
    assert process.stdout.strip() == stdout
