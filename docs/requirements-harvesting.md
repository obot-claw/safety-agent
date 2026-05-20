# Requirements Harvesting

## Source priority

1. Functional specs in the upstream wiki.
2. Data specification and settings schema.
3. Existing regression tests and test notes.
4. Example pages and default settings.
5. README and package metadata.
6. Historical issues/PRs if they clarify expected behavior.

## Extraction rules

- Split compound bullets into atomic requirements.
- Preserve exact clinical intent, but rewrite as testable statements.
- Keep a source URL or source file path for every requirement.
- Mark requirements as automated, manual, deferred, or unresolved.
- Do not silently drop requirements that depend on Webcharts behavior.

## Output format

Use the template in `templates/requirements-matrix.md`.
