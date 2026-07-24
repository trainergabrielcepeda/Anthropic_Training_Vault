---
paths: ["packages/api/src/routes/**/*", "packages/api/src/controllers/**/*"]
---

# API Route Conventions

Loads only for files under `packages/api/src/routes/**` or `packages/api/src/controllers/**` — frontend work in `packages/web` never pulls this in, keeping that context budget free for React/component conventions instead.

## Conventions

- Every route handler validates its input with the shared `zod` schema from `packages/shared/schemas` before touching business logic — never trust `req.body` directly.
- Errors are thrown as one of the typed errors in `packages/api/src/errors.ts` (`NotFoundError`, `ValidationError`, `ConflictError`) — never a bare `throw new Error(...)`, so the error-handling middleware can map them to correct HTTP status codes.
- Pagination uses cursor-based `?cursor=` + `?limit=`, never offset-based `?page=`, for any list endpoint.
- New routes are registered in `packages/api/src/routes/index.ts` and documented in `docs/api-reference.md` in the same PR — this is also called out as a universal standard in the root `CLAUDE.md`, but is repeated here because it's the rule most often missed when only this file is loaded.
