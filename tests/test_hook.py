"""Exercise package installation and scanning from a consumer repository."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def checked(*args: str, cwd: Path) -> str:
    result = run(*args, cwd=cwd)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


@pytest.fixture(scope="module")
def hook_repo(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, str]:
    repo = tmp_path_factory.mktemp("hook checkout")
    for name in ("pyproject.toml", "README.md", "LICENSE", ".pre-commit-hooks.yaml"):
        shutil.copy2(ROOT / name, repo / name)
    shutil.copytree(
        ROOT / "src", repo / "src", ignore=shutil.ignore_patterns("__pycache__")
    )
    checked("git", "init", "-q", cwd=repo)
    checked("git", "add", ".", cwd=repo)
    checked(
        "git",
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "-c",
        "core.hooksPath=/dev/null",
        "commit",
        "-qm",
        "fixture",
        cwd=repo,
    )
    return repo, checked("git", "rev-parse", "HEAD", cwd=repo)


@pytest.mark.parametrize("runner", ["pre-commit", "prek"])
def test_installed_hook(
    runner: str, hook_repo: tuple[Path, str], tmp_path: Path
) -> None:
    repo, revision = hook_repo
    checked("git", "init", "-q", cwd=tmp_path)
    (tmp_path / ".pre-commit-config.yaml").write_text(
        f"repos:\n  - repo: {json.dumps(str(repo))}\n    rev: {revision}\n"
        "    hooks:\n      - id: python-mock-hooks\n      - id: tests-without-ifs\n"
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "tests/test allowed.py").write_text(
        'monkeypatch.chdir("/tmp")\nmonkeypatch.setenv("X", "y")\n'
        'monkeypatch.delenv("X")\nmonkeypatch.undo()\n'
    )
    forbidden = 'monkeypatch.setattr(obj, "name", value)\n'
    forbidden_mock = "from unittest.mock import Mock as Fake\nFake()\n"
    forbidden_mocker = 'mocker.patch.object(service, "calculate", return_value=42)\n'
    (tmp_path / "src/ignored.py").write_text(
        forbidden + forbidden_mock + forbidden_mocker
    )
    (tmp_path / "tests/ignored.txt").write_text(forbidden)
    # A broken consumer config must not affect the packaged rule.
    (tmp_path / "sgconfig.yml").write_text("ruleDirs: [does-not-exist]\n")
    checked("git", "add", ".", cwd=tmp_path)
    checked(runner, "run", "python-mock-hooks", "--all-files", cwd=tmp_path)
    checked(runner, "run", "tests-without-ifs", "--all-files", cwd=tmp_path)
    (tmp_path / "tests/test forbidden.py").write_text(forbidden)
    checked("git", "add", ".", cwd=tmp_path)
    result = run(runner, "run", "python-mock-hooks", "--all-files", cwd=tmp_path)
    assert result.returncode != 0
    assert "no-forbidden-monkeypatch" in result.stdout + result.stderr
    assert "test forbidden.py" in result.stdout + result.stderr

    (tmp_path / "tests/test forbidden.py").write_text("pass\n")
    (tmp_path / "tests/test mock.py").write_text(forbidden_mock)
    checked("git", "add", ".", cwd=tmp_path)
    result = run(runner, "run", "python-mock-hooks", "--all-files", cwd=tmp_path)
    assert result.returncode != 0
    assert "no-unittest-mock" in result.stdout + result.stderr
    assert "test mock.py" in result.stdout + result.stderr

    (tmp_path / "tests/test mock.py").write_text("pass\n")
    (tmp_path / "tests/test mocker.py").write_text(forbidden_mocker)
    checked("git", "add", ".", cwd=tmp_path)
    result = run(runner, "run", "python-mock-hooks", "--all-files", cwd=tmp_path)
    assert result.returncode != 0
    assert "no-mocker-patch" in result.stdout + result.stderr
    assert "test mocker.py" in result.stdout + result.stderr
    checked(runner, "run", "tests-without-ifs", "--all-files", cwd=tmp_path)

    (tmp_path / "tests/test mocker.py").write_text("pass\n")
    (tmp_path / "tests/test branching.py").write_text(
        "def test_result():\n    if enabled:\n        assert result == 1\n"
    )
    checked("git", "add", ".", cwd=tmp_path)
    checked(runner, "run", "python-mock-hooks", "--all-files", cwd=tmp_path)
    result = run(runner, "run", "tests-without-ifs", "--all-files", cwd=tmp_path)
    assert result.returncode != 0
    assert "no-if-in-tests" in result.stdout + result.stderr
    assert "test branching.py" in result.stdout + result.stderr


@pytest.mark.parametrize("hook", ["python-mock-hooks", "tests-without-ifs"])
def test_no_filenames_does_not_scan(hook: str, tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text('monkeypatch.setattr(obj, "name", value)\n')
    checked(hook, cwd=tmp_path)


def test_no_uv_dependency(tmp_path: Path) -> None:
    # Give the command only ast-grep on PATH; neither uv nor uvx is available.
    command = shutil.which("python-mock-hooks")
    ast_grep = shutil.which("ast-grep")
    assert command is not None and ast_grep is not None
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    shutil.copy2(ast_grep, bin_dir / Path(ast_grep).name)
    bad_file = tmp_path / "bad.py"
    bad_file.write_text('monkeypatch.setattr(obj, "name", value)\n')
    result = subprocess.run(
        [command, str(bad_file)],
        cwd=tmp_path,
        env={**os.environ, "PATH": str(bin_dir)},
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert "no-forbidden-monkeypatch" in result.stdout + result.stderr
