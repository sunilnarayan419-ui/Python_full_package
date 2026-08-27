# 16_Debugging

Production debugging toolkit: structured exception-context capture
with local-variable snapshotting (`capture_failure_context`, useful
when a failure is only visible via aggregated logs), an
environment-variable-gated `breakpoint()` hook safe to leave in
production paths, always-on invariant assertions (unlike bare
`assert`), a batch processor that isolates and reports every malformed
record rather than failing opaquely on the first, and an async
pipeline that captures per-task failures via `asyncio.gather(...,
return_exceptions=True)`.

Run: `pytest tests/`
