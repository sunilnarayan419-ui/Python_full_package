# 19_Python_Internals

Practical uses of Python's object model: closures with `nonlocal` state
and `__closure__`/`co_freevars` introspection for a token-bucket rate
limiter; MRO-driven mixin composition (`CachingMixin` before
`RetryingMixin`) verified via `__mro__`; and `importlib`-based dynamic
plugin loading with `inspect.isclass` validation for
configuration-driven plugin systems.

Run: `pytest tests/`
