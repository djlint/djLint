<!--
Pull requests are squash-merged, so write the title in the Conventional Commits
style: `fix: ...`, `feat: ...`, `docs: ...`, `refactor: ...`, `test: ...`, `chore: ...`.
-->

## Summary

<!-- What does this change, and why? -->

## Related issues

<!-- `Closes #123` closes the issue on merge. Remove this section if there are none. -->

## Testing

<!-- How did you check that this works? -->

## Checklist

- [ ] `uvx prek run --all-files` passes.
- [ ] `uv run pytest` passes, and new behavior has tests.
- [ ] `CHANGELOG.md` describes any user-visible change under `[Unreleased]`.
- [ ] The docs are updated for changed behavior, in every language: `docs/src/docs/`, `docs/src/fr/docs/`, `docs/src/ru/docs/` and `docs/src/zh/docs/`.
- [ ] A new option is in `docs/src/_data/configuration.json` with its `since` version, and in `docs/src/static/schema/djlint.json`.
- [ ] A new rule is in `src/djlint/rules.yaml` or `src/djlint/rules/`, and in `docs/src/docs/linter.md` with examples.

<!-- If you have any questions about the points above, just submit and ask. This checklist is here to help you, not to deter you from contributing. -->
