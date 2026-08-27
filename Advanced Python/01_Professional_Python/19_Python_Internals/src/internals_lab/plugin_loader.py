"""Import-system internals applied to dynamic plugin loading: resolves
a dotted `module:ClassName` reference at runtime (e.g. from a
configuration file listing enabled analysis plugins), using
`importlib` directly rather than `__import__` for clearer error
semantics, and validates the loaded object via `inspect`.
"""
from __future__ import annotations

import importlib
import inspect
from typing import Any


class PluginLoadError(Exception):
    pass


def load_plugin_class(dotted_path: str) -> type[Any]:
    """Loads a class given `"package.module:ClassName"`. Using a fresh
    `importlib.import_module` call (rather than assuming the module is
    already in `sys.modules`) ensures plugins registered lazily via
    configuration are importable even if never explicitly imported
    elsewhere in the codebase.
    """
    if ":" not in dotted_path:
        raise PluginLoadError(f"expected 'module:ClassName', got {dotted_path!r}")
    module_name, _, class_name = dotted_path.partition(":")
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise PluginLoadError(f"could not import module {module_name!r}: {exc}") from exc
    try:
        plugin_class = getattr(module, class_name)
    except AttributeError as exc:
        raise PluginLoadError(f"module {module_name!r} has no attribute {class_name!r}") from exc
    if not inspect.isclass(plugin_class):
        raise PluginLoadError(f"{dotted_path} does not resolve to a class")
    return plugin_class
