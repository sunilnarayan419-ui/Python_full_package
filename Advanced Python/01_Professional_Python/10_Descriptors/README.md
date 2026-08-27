# 10_Descriptors

Reusable field descriptors for scientific/clinical domain models:
range-validated numeric fields (`BoundedFloat`), regex-validated string
identifiers (`ValidatedString`), a caching non-data descriptor
(`CachedProperty`), and a TTL-based lazy-loading data descriptor
(`LazyLoaded`) — the kind of cross-cutting field behavior that would
otherwise be duplicated as boilerplate `@property` methods across many
model classes.

Run: `pytest tests/`
