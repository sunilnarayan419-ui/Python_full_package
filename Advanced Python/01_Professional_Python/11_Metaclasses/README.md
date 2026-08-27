# 11_Metaclasses

Metaclass-based plugin registry for bioinformatics analysis models
(`AnalysisModelMeta`): every concrete subclass of `AnalysisModel` is
registered automatically under its `model_id`, with fail-fast
validation at class-definition time. Used only where genuine
architectural value exists — automatic, codebase-wide plugin discovery
that a decorator alone couldn't guarantee for every subclass.

Run: `pytest tests/`
