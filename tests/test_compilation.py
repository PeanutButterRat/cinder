import subprocess

import pytest

from cinder.cli import compile, parse
from os.path import join, dirname, realpath
import os

TEST_DIRECTORY = join(dirname(realpath(__file__)), "programs")
FILENAMES = [join(TEST_DIRECTORY, file) for file in os.listdir(TEST_DIRECTORY)]

@pytest.mark.parametrize("filepath", FILENAMES)
def test_compilation(filepath):
    file = open(filepath)
    source = file.read()
    stdout = source[:source.find('\n')].strip('/').strip()
    file.close()

    ast, globals = parse(source)
    compile(ast, globals)

    process = subprocess.run(["build/output.exe"], capture_output=True, text=True)

    assert process.returncode == 0
    assert process.stdout.strip() == stdout
