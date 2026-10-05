"""Run the bundled monkeypatch policy against explicit filenames."""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Forward filenames to ast-grep and preserve its exit status."""
    filenames = sys.argv[1:]
    if not filenames:
        return 0

    config = Path(__file__).with_name("sgconfig.yml")
    return subprocess.run(
        ["ast-grep", "scan", "--config", str(config), "--", *filenames],
        check=False,
    ).returncode
