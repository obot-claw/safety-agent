# Renderer requirements

Requirement matrices harvested from RhoInc wiki sources and passed through an AI sanity review.

| Renderer | Harvested rows | AI-reviewed rows kept | Removed/merged artifacts | Needs Jeremy review |
|---|---:|---:|---:|---:|
| [ae-timelines](./ae-timelines.md) | 55 | 43 | 12 | 6 |
| [aeexplorer](./aeexplorer.md) | 87 | 74 | 8 | 15 |
| [paneled-outlier-explorer](./paneled-outlier-explorer.md) | 126 | 114 | 12 | 9 |
| [safety-delta-delta](./safety-delta-delta.md) | 53 | 48 | 5 | 5 |
| [safety-histogram](./safety-histogram.md) | 126 | 121 | 5 | 27 |
| [safety-outlier-explorer](./safety-outlier-explorer.md) | 96 | 84 | 11 | 9 |
| [safety-results-over-time](./safety-results-over-time.md) | 68 | 58 | 10 | 6 |
| [safety-shift-plot](./safety-shift-plot.md) | 47 | 39 | 8 | 7 |
| [web-codebook](./web-codebook.md) | 228 | 223 | 2 | 22 |

## Review sequence

1. AI review marks standalone rows as `ai-reviewed` and ambiguous rows as `needs-jeremy-review`.
2. Jeremy reviews flagged rows through the grill-me/interview workflow, starting with the renderer that will be implemented next.
3. After decisions, rows move to `reviewed`, then implementation/evidence statuses.
