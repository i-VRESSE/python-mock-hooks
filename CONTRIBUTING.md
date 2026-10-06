# Contributing

## Development

Use uv to create the virtual environment and install the project and its
development dependencies:

```sh
uv sync
```

Neither uv nor the development tools are dependencies of the installed hook.

- Rules and configuration are bundled with the package; consumers don't need
  `sgconfig.yml`.
- Matching is syntactic: rules don't resolve types, follow aliases, or trace
  imports to their uses.

```sh
uv run prek validate-manifest .pre-commit-hooks.yaml
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
