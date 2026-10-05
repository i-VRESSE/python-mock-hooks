# Contributing

## Development

Install the project and development tools in a virtual environment:

```sh
python -m pip install -e . pytest pre-commit prek pyrefly
```

Alternatively, `uv sync` installs the project and its development dependency group.
Neither uv nor the development tools are dependencies of the installed hook.

```sh
ast-grep test --config sgconfig.yml
python -m pytest
pyrefly check
prek run --all-files
```

The rule and its test cases originated in protein-quest. Keep changes to the
policy covered by valid and invalid examples in `tests/`.
The pytest integration tests install a temporary copy of this repository
through both pre-commit and prek. They check the packaged rule, filename
filtering, failures, and paths with spaces without staging or committing files
in this repository. Git and network access for installation are required.

To change the ast-grep version, update `pyproject.toml` and the development
rule-test hook in `.pre-commit-config.yaml`, then rerun the checks.
Publish a tag after committing a release so consumers can pin it and use
`prek autoupdate` or `pre-commit autoupdate` for subsequent updates.
There is no need to publish the package to PyPI.

## Implementation

The hook uses `language: python`. Pre-commit or prek installs the package and
its pinned `ast-grep-cli` dependency from `pyproject.toml` into an isolated
environment. Installation requires network access; ast-grep's available
platform wheels determine platform support.

The `check-monkeypatch` entry point in `src/check_monkeypatch/__init__.py`
locates the bundled YAML rule using `importlib.resources` and runs
`ast-grep scan --rule` with its absolute path. It forwards the filenames
supplied by the hook runner and returns ast-grep's exit status. With no
filenames, it exits successfully without scanning the working directory.

The rule lives in `src/check_monkeypatch/rules/` and is included in the
installed package. Consumers do not need a local `sgconfig.yml`; their
working directory and ast-grep configuration do not determine which rule
runs. This repository's `sgconfig.yml` is used to run the rule tests.

The policy matches calls literally written as `monkeypatch.METHOD(...)`
and permits `chdir`, `setenv`, `delenv`, and `undo`. It does not resolve
aliases or types, so unrelated objects named `monkeypatch` are also checked.
Changes to environment variables and the working directory are intentionally
allowed. This hook does not detect `unittest.mock` or `mocker.patch`.
