# check-monkeypatch

A pre-commit / prek hook that restricts pytest `monkeypatch` calls to:

- `monkeypatch.chdir`
- `monkeypatch.setenv`
- `monkeypatch.delenv`
- `monkeypatch.undo`

Other methods, including `setattr`, `delattr`, `setitem`, `delitem`,
`syspath_prepend`, and `context`, fail the check. For HTTP tests, prefer
recording and replaying requests with pytest-recording.

## Usage

Add the following to your `.pre-commit-config.yaml`, replacing the repository
URL and revision with where you publish this repository and its release tag
or commit SHA:

```yaml
repos:
  - repo: https://github.com/YOUR-ORG/check-monkeypatch
    rev: YOUR-TAG-OR-COMMIT
    hooks:
      - id: check-monkeypatch
```

Then run `prek run check-monkeypatch --all-files` or
`pre-commit run check-monkeypatch --all-files`.

The hook uses `language: python`. Your hook runner installs this package and
its pinned `ast-grep-cli` dependency automatically in an isolated environment.
No uv, shell launcher, manual ast-grep installation, or project-local
`sgconfig.yml` is needed. Use Python 3.10 or newer; first installation requires
network access. ast-grep's available platform wheels determine platform support.

By default, the hook checks Python files under `tests/`. Override `files`
for another layout, for example `files: ^(tests|test)/.*\.py$`.
The rule is bundled in the installed package, so it does not depend on the
consumer's working directory or ast-grep configuration.

## Scope

This is a syntax check for calls literally written as `monkeypatch.METHOD(...)`.
It does not resolve aliases or types, and does not detect `unittest.mock`,
`mocker.patch`, or calls through a differently named variable. It also rejects
methods on unrelated objects named `monkeypatch`. It intentionally permits
changes to the environment and working directory.

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

## License

Apache-2.0; see [LICENSE](LICENSE). The rule and rule tests were copied from
[protein-quest](https://github.com/haddocking/protein-quest).
