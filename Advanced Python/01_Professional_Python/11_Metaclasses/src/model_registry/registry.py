"""Metaclass-based auto-registration for pluggable bioinformatics
analysis models (e.g. variant-effect predictors, QC scorers).

A metaclass is justified here — rather than a simple decorator — because
we need every *subclass*, anywhere in the codebase or in third-party
plugin packages, to be registered automatically at class-definition
time without each author remembering to call a registration function,
and because we also validate the subclass's shape (required class
attributes) at definition time rather than at first use.
"""
from __future__ import annotations

import abc
from typing import Any, ClassVar


class ModelRegistrationError(Exception):
    pass


class ModelRegistry:
    """Central registry populated automatically by `AnalysisModelMeta`."""

    _models: ClassVar[dict[str, type["AnalysisModel"]]] = {}

    @classmethod
    def register(cls, model_id: str, model_cls: type["AnalysisModel"]) -> None:
        if model_id in cls._models:
            raise ModelRegistrationError(f"model_id {model_id!r} already registered")
        cls._models[model_id] = model_cls

    @classmethod
    def get(cls, model_id: str) -> type["AnalysisModel"]:
        try:
            return cls._models[model_id]
        except KeyError as exc:
            raise ModelRegistrationError(f"no model registered under {model_id!r}") from exc

    @classmethod
    def available(cls) -> tuple[str, ...]:
        return tuple(sorted(cls._models))


class AnalysisModelMeta(abc.ABCMeta):
    """Registers every concrete (non-abstract) subclass under its
    declared `model_id`, and validates required metadata at
    class-definition time so misconfigured plugins fail fast at import
    rather than at first invocation.
    """

    def __new__(
        mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kwargs: Any
    ) -> "AnalysisModelMeta":
        new_class = super().__new__(mcs, name, bases, namespace, **kwargs)
        is_abstract = namespace.get("__abstractmethods__") or getattr(
            new_class, "__abstractmethods__", None
        )
        model_id = namespace.get("model_id")
        if bases and not is_abstract:
            if not model_id or not isinstance(model_id, str):
                raise ModelRegistrationError(
                    f"{name} must define a non-empty string class attribute 'model_id'"
                )
            ModelRegistry.register(model_id, new_class)  # type: ignore[arg-type]
        return new_class


class AnalysisModel(abc.ABC, metaclass=AnalysisModelMeta):
    """Base class for pluggable analysis models. Subclassing and
    defining `model_id` is sufficient for automatic registry
    availability system-wide.
    """

    model_id: ClassVar[str]

    @abc.abstractmethod
    def score(self, sequence: str) -> float:
        """Return a model-specific score for the given sequence."""


def register_analysis_model(model_id: str):  # noqa: ANN201
    """Alternative explicit-decorator registration path, for cases where
    inheritance-based auto-registration is undesirable (e.g. wrapping a
    third-party callable that cannot subclass `AnalysisModel`).
    """

    def decorator(model_cls: type[AnalysisModel]) -> type[AnalysisModel]:
        ModelRegistry.register(model_id, model_cls)
        return model_cls

    return decorator
