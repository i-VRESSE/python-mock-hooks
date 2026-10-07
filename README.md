# python-mock-hooks

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23183666.svg)](https://doi.org/10.5281/zenodo.23183666)
[![Research Software Directory Badge](https://img.shields.io/badge/rsd-00a3e3.svg)](https://research-software-directory.org/software/python-mock-precommit-hook)

Two independently selectable pre-commit / prek hooks for Python tests.

### `python-mock-hooks`

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

### `tests-without-ifs`

Blocks `if` / `elif` / `else` branching statements inside `test_*` functions
and methods, including async tests. Use separate tests or
`pytest.mark.parametrize` for each case instead.

Permits `if` statements in fixtures, helpers (including nested helpers), and
at module or class scope, as well as conditional expressions
(`a if condition else b`) and comprehension filters. This hook does not
restrict mocking; `python-mock-hooks` does not restrict branching.

Check failures explain the policy to developers and LLM coding agents.

Ruff [does not support custom lint plugins](https://docs.astral.sh/ruff/faq/#can-i-write-my-own-linter-plugins-for-ruff),
so these hooks add testing policies as separate checks alongside Ruff.

## Usage

Requires Python 3.11 or newer. Dependencies are installed automatically.
Choose one configuration format, replacing the revision with a release tag
or commit SHA.

For `.pre-commit-config.yaml` (pre-commit or prek):

```yaml
repos:
  - repo: https://github.com/i-VRESSE/python-mock-hooks
    rev: v0.3.0
    hooks:
      - id: python-mock-hooks
      - id: tests-without-ifs
```

For `prek.toml` (prek):

```toml
[[repos]]
repo = "https://github.com/i-VRESSE/python-mock-hooks"
rev = "v0.3.0"
hooks = [{ id = "python-mock-hooks" }, { id = "tests-without-ifs" }]
```

Enable either hook or both. Run `prek run --all-files` to run all enabled hooks
(or use `pre-commit` instead of `prek`).

Both hooks check Python files under `tests/` by default. For another layout,
set `files` on each enabled hook:

- YAML: `files: ^(tests|test)/.*\.py$`
- TOML: `files = '^(tests|test)/.*\.py$'`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and implementation details.

## Acknowledgments

Rule and rule tests adapted from
[protein-quest](https://github.com/haddocking/protein-quest).
Inspired by [PFCCLab/ast-grep-pre-commit-mirror](https://github.com/PFCCLab/ast-grep-pre-commit-mirror/).

## License

[Apache-2.0](LICENSE).
