---
paths: ["**/*.test.ts", "**/*.test.tsx"]
---

# Test File Conventions

This rule loads only when Claude Code is reading or editing a file matching `**/*.test.ts` or `**/*.test.tsx` — not on every turn, and regardless of which directory the test file lives in (unit tests sit next to the code they cover throughout `packages/api` and `packages/web`, so a directory-scoped `CLAUDE.md` couldn't cover all of them without duplication).

## Conventions

- Use `describe` / `it`, never the bare `test()` alias.
- Mock outbound HTTP with the shared `mockFetch` helper from `packages/shared/test-utils` — do not hand-roll `jest.mock('node-fetch')` per file.
- Every test file must include at least one failure-path assertion (not just the happy path).
- Snapshot tests require a one-line comment explaining what invariant the snapshot protects — bare snapshots without justification are rejected in review.
- Async assertions must use `await expect(...).rejects/resolves`, never a bare `.catch()`.
