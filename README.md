# [check-monkeypatch](https://github.com/i-VRESSE/check-monkeypatch)

A pre-commit / prek hook that allows only these pytest `monkeypatch` methods:
`chdir`, `setenv`, `delenv`, and `undo`. All other methods fail the check.
For HTTP tests, prefer recording requests with
[pytest-recording](https://github.com/kiwicom/pytest-recording).

The hook also gives LLM coding agents feedback when they run the checks:
disallowed pytest `monkeypatch` calls, such as `monkeypatch.setattr`, fail
with a message explaining which methods are allowed and pointing to
pytest-recording for HTTP tests. This helps steer generated tests away from
unwanted mocking.

Ruff [does not support custom lint plugins](https://docs.astral.sh/ruff/faq/#can-i-write-my-own-linter-plugins-for-ruff),
so this hook adds the monkeypatch policy as a separate check alongside Ruff.

## Usage

Requires Python 3.10 or newer. Dependencies are installed automatically.
Add this to `.pre-commit-config.yaml`, replacing the revision with a release
tag or commit SHA:

```yaml
repos:
  - repo: https://github.com/i-VRESSE/check-monkeypatch
    rev: YOUR-TAG-OR-COMMIT
    hooks:
      - id: check-monkeypatch
```

Run `prek run check-monkeypatch --all-files` (or use `pre-commit` instead of `prek`).

Checks Python files under `tests/` by default. For another layout, set
`files`, for example `files: ^(tests|test)/.*\.py$`.

Only calls written as `monkeypatch.METHOD(...)` are checked, regardless of the
object's type. Aliases, `unittest.mock`, and `mocker.patch` are not detected.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and implementation details.

## License

[Apache-2.0](LICENSE). Rule and rule tests adapted from
[protein-quest](https://github.com/haddocking/protein-quest).
