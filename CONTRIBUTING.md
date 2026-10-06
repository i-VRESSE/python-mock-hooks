# Contributing

## Development

Use uv to create the virtual environment and install the project and its
development dependencies:

```sh
uv sync
```

Neither uv nor the development tools are dependencies of the installed hook.

```sh
uv run ast-grep test --config sgconfig.yml
uv run pytest
uv run pyrefly check
uv run prek run --all-files
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
`uv run prek autoupdate` or `uv run pre-commit autoupdate` for subsequent updates.
There is no need to publish the package to PyPI.

## Implementation

The hook uses `language: python`. Pre-commit or prek installs the package and
its pinned `ast-grep-cli` dependency from `pyproject.toml` into an isolated
environment. Installation requires network access; ast-grep's available
platform wheels determine platform support.

The `python-mock-hooks` entry point in `src/python_mock_hooks/__init__.py`
locates the bundled `sgconfig.yml` beside the installed module and runs
`ast-grep scan --config` with its absolute path. It forwards the filenames
supplied by the hook runner and returns ast-grep's exit status. With no
filenames, it exits successfully without scanning the working directory.

The static rules live in `src/python_mock_hooks/rules/` and are included in
the installed package with its configuration. Consumers do not need a local
`sgconfig.yml`; their working directory and ast-grep configuration do not
determine which rules run. The root `sgconfig.yml` adds the rule-test directory
for development.

The monkeypatch policy matches calls literally written as
`monkeypatch.METHOD(...)` and permits `chdir`, `setenv`, `delenv`, and `undo`.
It does not resolve aliases or types, so unrelated objects named
`monkeypatch` are also checked. Changes to environment variables and the
working directory are intentionally allowed.

The `no-unittest-mock` rule rejects imports of `unittest.mock`, imports from
that module, `from unittest import mock`, and direct `unittest.mock`
references. Import checks catch aliases, multiple imports, and multiline
imports without tracing subsequent calls. Unused imports are also rejected.
Ordinary `unittest` and `TestCase` imports remain allowed.

The `no-mocker-patch` rule rejects `patch` attribute references on `mocker`
and its `class_mocker`, `module_mocker`, `package_mocker`, and `session_mocker`
variants. Matching the attribute also catches chained forms such as
`mocker.patch.object` and assignments such as `replace = mocker.patch`.
Other pytest-mock APIs remain allowed.

These are syntax rules, not name resolution: dynamic imports, re-exports,
`import unittest as ut; ut.mock.Mock()`, and renamed mocker fixtures are
outside their scope. Local objects with the checked names and attributes
are also matched.
