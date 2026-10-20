# Naming options

The repository contains two independently selectable Python test policies:

- Restrict `unittest.mock`, `mocker.patch`, and most `monkeypatch` methods.
- Reject `if` statements inside `test_*` functions and methods.

Compatibility is not a requirement. The options below assume a clean rename,
without legacy hook IDs or command aliases.

## Examples from established hooks

Existing projects use several naming patterns rather than one uniform convention:

- Actions: `check-ast`, `detect-private-key`, and `check-builtin-literals` in
  [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks/blob/main/.pre-commit-hooks.yaml).
- Prohibitions with a language prefix: `python-no-eval` and
  `python-no-log-warn` in
  [pygrep-hooks](https://github.com/pre-commit/pygrep-hooks/blob/main/.pre-commit-hooks.yaml).
- Tool and action: `ruff-check` and `ruff-format` in
  [ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit/blob/main/.pre-commit-hooks.yaml).

These examples support short, descriptive hook IDs with hyphens. A collection's
repository name can describe its overall purpose while each hook ID describes
one policy.

## Repository names

| Name | Pros | Cons |
| --- | --- | --- |
| **`python-test-hooks`** | Clearly identifies the language and purpose; accommodates additional test policies. | Broad; does not emphasize that the rules are opinionated. |
| `python-test-policy-hooks` | Explicitly describes selectable testing policies. | Longer and less convenient to type. |
| `python-test-pre-commit` | Makes the integration immediately obvious, following the `ruff-pre-commit` pattern. | Less natural if the commands also become standalone lint tools. |
| `python-test-lint` | Concise; describes static checks and suits standalone use. | Does not advertise the pre-commit integration. |
| `python-mock-hooks` | Short and accurately describes the original mocking policy. | Does not describe the new conditional-statement hook or future unrelated policies. |

## Mocking hook alternatives to `python-mock-hooks`

The policy permits `mocker.Mock`, `mocker.spy`, and several `monkeypatch` methods.
Its name should therefore describe restrictions rather than promise a complete
ban on mocks.

| Hook ID | Pros | Cons |
| --- | --- | --- |
| **`check-test-mocking`** | Uses the established `check-*` pattern; covers all three mocking APIs without claiming a total ban. | The exact restrictions require a description. |
| `restrict-test-mocking` | Clearly communicates selective restrictions and test scope. | `restrict-*` is less familiar than the patterns in the examples above. |
| `check-mocking-policy` | Accurately communicates an opinionated policy with exceptions. | Omits test scope and is somewhat abstract. |
| `python-check-test-mocking` | Explicit language and test scope; follows the language-prefix pattern used by pygrep-hooks. | Longer; Python is already present in the recommended repository name. |
| `no-patching-in-tests` | Directly communicates the main discouraged behavior. | Overstates the policy because environment and working-directory monkeypatching are allowed; also understates the ban on `unittest.mock` imports. |
| `tests-with-restricted-mocking` | Reads naturally and pairs with `tests-without-ifs`. | Long and less consistent with common action-based hook IDs. |

Avoid `no-mocks` and `tests-without-mocks`: both imply that all mocking is
forbidden, which does not match the implementation.

## Conditional-statement hook names

| Hook ID | Pros | Cons |
| --- | --- | --- |
| **`no-if-in-tests`** | Direct; follows the prohibition pattern; matches the existing rule ID. | Its description should clarify that conditional expressions remain allowed. |
| `python-no-if-in-tests` | Explicit language scope; follows pygrep-hooks naming. | Longer and repeats the language in the recommended repository name. |
| `tests-without-ifs` | Readable and already used by the new hook. | Less consistent with the action and prohibition patterns above; `ifs` is informal. |
| `check-test-if-statements` | Uses `check-*` and precisely identifies the syntax being checked. | Does not immediately communicate that every matching statement is forbidden. |
| `check-test-conditionals` | Concise and uses the established `check-*` pattern. | Suggests coverage of conditional expressions and comprehension filters, which are allowed. |
| `no-test-branching` | Communicates the policy's motivation. | Overstates coverage: `match`, conditional expressions, and other control flow remain allowed. |

## Suggested combinations

| Style | Repository | Mocking hook | Conditional-statement hook | Tradeoff |
| --- | --- | --- | --- | --- |
| **Recommended** | `python-test-hooks` | `check-test-mocking` | `no-if-in-tests` | Short, descriptive names; each hook uses the wording that best fits its actual policy. |
| Explicit language | `python-test-hooks` | `python-check-test-mocking` | `python-no-if-in-tests` | Hook IDs make sense outside the repository context, at the cost of length. |
| Consistent actions | `python-test-policy-hooks` | `check-test-mocking` | `check-test-if-statements` | Both IDs follow `check-*`; the prohibition is expressed in the hook description. |
| Natural phrasing | `python-test-hooks` | `tests-with-restricted-mocking` | `tests-without-ifs` | Both names describe the desired tests; the mocking ID is lengthy. |

With the recommended names, the consumer configuration would be:

```yaml
repos:
  - repo: https://github.com/i-VRESSE/python-test-hooks
    rev: v0.3.0
    hooks:
      - id: check-test-mocking
      - id: no-if-in-tests
```

These are proposals; repository, package, command, and hook names have not been
changed. Once a combination is selected, the rename should update the GitHub
repository, package metadata and import path, console commands, hook manifest,
documentation, and integration tests together.
