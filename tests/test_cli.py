import shutil
import subprocess
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent


def test_map_empty_mappings(out_dir):
    run_cli(f"data/mapEmptyMappings.js.map -o {out_dir}")
    assert_diff("tests/goldens/mapEmptyMappings", out_dir)


def test_map_with_sources_content(out_dir):
    run_cli(f"data/mapWithSourcesContent.js.map -o {out_dir}")
    assert_diff("tests/goldens/mapWithSourcesContent", out_dir)


@pytest.fixture
def out_dir() -> Path:
    out_dir = TESTS_DIR / "out"
    shutil.rmtree(out_dir)
    return out_dir


def run_cli(arg_str: str):
    subprocess.run(
        ["python", "-m", "py_unpack_sourcemap", *arg_str.split()],
        check=True,
        cwd=TESTS_DIR,
    )


def assert_diff(golden_path: str, output_path: Path):
    proc = subprocess.run(
        ["diff", "-r", golden_path, output_path],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    if proc.returncode:
        pytest.fail("Output diff failed (see stdout)")
