"""Run the bundled testing policies against explicit filenames."""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Check mocking policies."""
    return _scan("sgconfig.yml")


def tests_without_ifs() -> int:
    """Check for if statements in test bodies."""
    return _scan("ifs-sgconfig.yml")


def _scan(config_name: str) -> int:
    """Forward filenames to ast-grep and preserve its exit status."""
    filenames = sys.argv[1:]
    if not filenames:
        return 0

    config = Path(__file__).with_name(config_name)
    return subprocess.run(
        ["ast-grep", "scan", "--config", str(config), "--", *filenames],
        check=False,
    ).returncode
