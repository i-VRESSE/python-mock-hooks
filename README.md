# [python-mock-hooks](https://github.com/i-VRESSE/python-mock-hooks)

A pre-commit / prek hook that allows only these pytest `monkeypatch` methods:
`chdir`, `setenv`, `delenv`, and `undo`. All other methods fail the check.
It also forbids `unittest.mock` imports and direct references, including
`Mock`, `MagicMock`, `AsyncMock`, and `patch` imported from that module.
For HTTP tests, prefer recording requests with
[pytest-recording](https://github.com/kiwicom/pytest-recording).

The hook also gives LLM coding agents feedback when they run the checks:
disallowed pytest `monkeypatch` calls, such as `monkeypatch.setattr`, fail
with a message explaining which methods are allowed and pointing to
pytest-recording for HTTP tests. This helps steer generated tests away from
unwanted mocking.

Ruff [does not support custom lint plugins](https://docs.astral.sh/ruff/faq/#can-i-write-my-own-linter-plugins-for-ruff),
so this hook adds these testing policies as a separate check alongside Ruff.

## Usage

Requires Python 3.11 or newer. Dependencies are installed automatically.
Add this to `.pre-commit-config.yaml`, replacing the revision with a release
tag or commit SHA:

```yaml
repos:
  - repo: https://github.com/i-VRESSE/python-mock-hooks
    rev: v0.1.0
    hooks:
      - id: python-mock-hooks
```

Run `prek run python-mock-hooks --all-files` (or use `pre-commit` instead of `prek`).

Checks Python files under `tests/` by default. For another layout, set
`files`, for example `files: ^(tests|test)/.*\.py$`.

The monkeypatch rule checks calls written as `monkeypatch.METHOD(...)`,
regardless of the object's type. The `unittest.mock` rule rejects imports
even when aliased or unused. Dynamic imports, indirect references through
other modules, and `mocker.patch` are not detected.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and implementation details.

## Acknowledgments

Rule and rule tests adapted from
[protein-quest](https://github.com/haddocking/protein-quest).
Inspired by [PFCCLab/ast-grep-pre-commit-mirror](https://github.com/PFCCLab/ast-grep-pre-commit-mirror/).

## License

[Apache-2.0](LICENSE).
