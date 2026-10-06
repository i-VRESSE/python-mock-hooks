# [python-mock-hooks](https://github.com/i-VRESSE/python-mock-hooks)

A pre-commit / prek hook that restricts mocking in Python tests:

- **Blocks**:
  - `unittest.mock` imports and references.
  - `mocker.patch` and `mocker.patch.*` usage from [pytest-mock](https://github.com/pytest-dev/pytest-mock)
  - All `monkeypatch` pytest methods except those permitted below.
- **Permits**:
  - `monkeypatch.chdir`
  - `monkeypatch.setenv`
  - `monkeypatch.delenv`
  - `monkeypatch.undo`
  - `mocker.Mock`, `mocker.spy`, and other pytest-mock APIs besides `patch`.

For HTTP tests, prefer recording requests with
[pytest-recording](https://github.com/kiwicom/pytest-recording).

Check failures explain the policy to developers and LLM coding agents.

Ruff [does not support custom lint plugins](https://docs.astral.sh/ruff/faq/#can-i-write-my-own-linter-plugins-for-ruff),
so this hook adds these testing policies as a separate check alongside Ruff.

## Usage

Requires Python 3.11 or newer. Dependencies are installed automatically.
Add this to `.pre-commit-config.yaml`, replacing the revision with a release
tag or commit SHA:

```yaml
repos:
  - repo: https://github.com/i-VRESSE/python-mock-hooks
    rev: v0.2.0
    hooks:
      - id: python-mock-hooks
```

Run `prek run python-mock-hooks --all-files` (or use `pre-commit` instead of `prek`).

Checks Python files under `tests/` by default. For another layout, set
`files`, for example `files: ^(tests|test)/.*\.py$`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and implementation details.

## Acknowledgments

Rule and rule tests adapted from
[protein-quest](https://github.com/haddocking/protein-quest).
Inspired by [PFCCLab/ast-grep-pre-commit-mirror](https://github.com/PFCCLab/ast-grep-pre-commit-mirror/).

## License

[Apache-2.0](LICENSE).
