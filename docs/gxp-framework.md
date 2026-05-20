# GxP-Oriented Framework

## Objective

Create enough traceability and evidence that renderer behavior can be reviewed, audited, and eventually qualified in a project-specific validation process.

## Requirement sources

Use all available upstream sources:

- RhoInc wiki technical documentation
- functional specs sections
- data guidelines pages
- configuration/settings wiki pages
- `settings-schema.json`
- README examples
- test-page fixtures
- existing statistical regression tests
- issue/PR history when relevant

## Requirement IDs

Use stable IDs:

- `SH-DATA-###` for data shape and mapping requirements
- `SH-CTRL-###` for controls
- `SH-CHART-###` for chart rendering behavior
- `SH-LIST-###` for listing/detail behavior
- `SH-STAT-###` for statistical tests and annotations
- `SH-WARN-###` for warnings/errors
- `SH-A11Y-###` for accessibility
- `SH-PERF-###` for performance/responsiveness

Replace `SH` with a renderer-specific prefix for other packages.

## Evidence classes

- `unit` - deterministic code-level test
- `integration` - renderer API or DOM integration test
- `browser` - end-to-end browser behavior test
- `visual` - screenshot/image comparison
- `manual` - documented manual review where automation is not yet practical
- `deferred` - requirement accepted but intentionally not implemented in the current phase

## Change control expectations

Each PR should include:

- requirement IDs addressed
- tests added/updated
- screenshots or visual evidence when rendering changes
- compatibility notes
- known gaps
- reviewer checklist
