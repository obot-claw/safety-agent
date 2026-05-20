# Test Framework

## Test pyramid

1. Unit tests for pure functions.
2. Integration tests for renderer lifecycle and DOM/canvas output.
3. Browser tests for user behavior.
4. Visual regression tests for display stability.
5. Requirements traceability checks.

## Recommended tooling

- Test runner: Vitest or Jest for unit/integration tests.
- Browser automation: Playwright for functional browser tests and screenshots.
- Visual regression: Playwright screenshots with thresholded comparisons.
- Static checks: ESLint, Prettier, TypeScript or JSDoc types where feasible.
- Build: Vite/Rollup modern build pipeline.

## Requirements-driven test pattern

Each test file should reference requirement IDs in test names or metadata. Example:

```js
test('SH-CTRL-001 measure filter changes the displayed distribution', async () => {
  // test steps
});
```

## Existing Safety Histogram requirements to preserve

From the upstream technical documentation, the replacement renderer needs tests for:

- measure selection changes the distribution
- participant count annotation updates under filtering
- normal range display toggles without changing axes
- x-axis limit controls, reset, and validation
- missing/non-numeric records are removed and reported
- invalid settings generate warnings or visible errors as appropriate
- bin quantity, bin width, and bin algorithm controls stay synchronized
- linear versus bin-boundary x-axis tick behavior
- hover footnotes and bar highlighting
- click-through detail listing
- grouped/small-multiple histogram behavior
- normality and distribution comparison p-value annotations
