from __future__ import annotations

import io
import itertools

from streaming import (
    BoundedBuffer,
    iter_fastq_records,
    quality_filter,
    running_stats,
    sliding_window_gc,
)

_SAMPLE_FASTQ = (
    "@read1\nACGTACGTAC\n+\nIIIIIIIIII\n"
    "@read2\nGGGGCCCCAA\n+\n!!!!!!!!!!\n"
)


def test_iter_fastq_records_is_lazy_and_correct() -> None:
    stream = io.StringIO(_SAMPLE_FASTQ)
    records = list(iter_fastq_records(stream))
    assert len(records) == 2
    assert records[0].identifier == "read1"
    assert records[1].sequence == "GGGGCCCCAA"


def test_quality_filter_drops_low_quality_records() -> None:
    stream = io.StringIO(_SAMPLE_FASTQ)
    records = list(iter_fastq_records(stream))
    filtered = list(quality_filter(records, min_mean_quality=30.0))
    assert [r.identifier for r in filtered] == ["read1"]


def test_running_stats_matches_naive_computation() -> None:
    values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    *_, (final_count, final_mean, final_variance) = running_stats(values)
    assert final_count == len(values)
    assert round(final_mean, 4) == round(sum(values) / len(values), 4)
    naive_variance = sum((v - final_mean) ** 2 for v in values) / len(values)
    assert round(final_variance, 4) == round(naive_variance, 4)


def test_sliding_window_gc_windows_sequence() -> None:
    stream = io.StringIO("@r\n" + "G" * 100 + "\n+\n" + "I" * 100 + "\n")
    records = list(iter_fastq_records(stream))
    windows = list(sliding_window_gc(records, window=50))
    assert windows[0][1] == [1.0, 1.0]


def test_bounded_buffer_yields_all_items_in_order() -> None:
    source = range(10)
    buffer = BoundedBuffer(capacity=3)
    assert list(buffer.throttle(source)) == list(range(10))


def test_pipeline_never_materializes_full_generator_early() -> None:
    """Demonstrates laziness: an infinite generator can be safely piped
    through `quality_filter` as long as consumption is bounded.
    """

    def infinite_records():
        for i in itertools.count():
            yield type("R", (), {"quality": "I" * 10, "sequence": "ACGT", "identifier": str(i)})()

    filtered = quality_filter(infinite_records(), min_mean_quality=1.0)
    first_five = list(itertools.islice(filtered, 5))
    assert [r.identifier for r in first_five] == ["0", "1", "2", "3", "4"]
