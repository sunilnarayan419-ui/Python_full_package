from __future__ import annotations

import gc
import io
import weakref

from lifecycle import PipelineStage, ResourceLeakDetector, TrackedFileHandle


class _RecordingObserver:
    def __init__(self) -> None:
        self.completed_stages: list[str] = []

    def on_stage_complete(self, stage: PipelineStage, *, records_processed: int) -> None:
        self.completed_stages.append(stage.name)


def test_stage_notifies_live_observer() -> None:
    observer = _RecordingObserver()
    stage = PipelineStage("alignment", observer=observer)
    stage.run([b"read1", b"read2"])
    assert observer.completed_stages == ["alignment"]


def test_stage_does_not_keep_observer_alive() -> None:
    observer = _RecordingObserver()
    observer_ref = weakref.ref(observer)
    stage = PipelineStage("variant_calling", observer=observer)
    del observer
    gc.collect()
    assert observer_ref() is None
    stage.run([b"data"])  # must not raise even though observer is gone


def test_tracked_file_handle_detects_unclosed_resource() -> None:
    leaks: list[str] = []
    handle = TrackedFileHandle(io.BytesIO(b"data"), on_leak=leaks.append)
    handle_ref = weakref.ref(handle)
    del handle
    ResourceLeakDetector.object_is_alive(handle_ref)
    gc.collect()
    assert leaks, "expected a leak to be reported for an unclosed handle"


def test_tracked_file_handle_context_manager_does_not_leak() -> None:
    leaks: list[str] = []
    with TrackedFileHandle(io.BytesIO(b"data"), on_leak=leaks.append) as handle:
        assert handle is not None
    gc.collect()
    assert leaks == []
