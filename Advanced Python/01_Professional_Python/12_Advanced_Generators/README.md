# 12_Advanced_Generators

Streaming FASTQ processing pipeline demonstrating why generators beat
materialization for large scientific datasets: lazy parsing
(`iter_fastq_records`), composable filter/transform stages
(`quality_filter`, `sliding_window_gc`), an online-statistics generator
using Welford's algorithm (`running_stats`, O(1) memory regardless of
stream length), and a bounded-buffer backpressure sink (`BoundedBuffer`).

Run: `pytest tests/`
