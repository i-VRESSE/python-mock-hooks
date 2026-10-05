"""Run the bundled monkeypatch policy against explicit filenames."""

import subprocess
import sys
from importlib.resources import as_file, files


def main() -> int:
    """Forward filenames to ast-grep and preserve its exit status."""
    filenames = sys.argv[1:]
    if not filenames:
        return 0

    rule = files("check_monkeypatch").joinpath("rules/no-forbidden-monkeypatch.yml")
    with as_file(rule) as rule_path:
        return subprocess.run(
            ["ast-grep", "scan", "--rule", str(rule_path), "--", *filenames],
            check=False,
        ).returncode
