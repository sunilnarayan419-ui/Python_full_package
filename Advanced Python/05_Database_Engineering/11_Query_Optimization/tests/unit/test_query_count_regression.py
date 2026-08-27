from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.repositories.experiment_repository import ExperimentRepositoryAfter, ExperimentRepositoryBefore


@pytest.mark.asyncio
async def test_before_variant_issues_one_query_per_experiment() -> None:
    session = AsyncMock()

    class FakeExperiment:
        def __init__(self, eid: int) -> None:
            self.experiment_id = eid
            self.title = f"Experiment {eid}"

    experiments = [FakeExperiment(1), FakeExperiment(2), FakeExperiment(3)]

    call_results = [experiments, [1], [1, 2], []]

    async def fake_execute(*_args, **_kwargs):
        result = AsyncMock()
        result.scalars.return_value.all.return_value = call_results.pop(0)
        return result

    session.execute.side_effect = fake_execute

    repo = ExperimentRepositoryBefore(session)
    summaries = await repo.list_summaries()

    assert len(summaries) == 3
    # 1 query for experiments + 3 queries for jobs = 4 total round trips for 3 experiments.
    assert session.execute.await_count == 4


@pytest.mark.asyncio
async def test_after_variant_issues_a_constant_number_of_queries() -> None:
    session = AsyncMock()

    class FakeJob:
        pass

    class FakeExperiment:
        def __init__(self, eid: int, job_count: int) -> None:
            self.experiment_id = eid
            self.title = f"Experiment {eid}"
            self.analysis_jobs = [FakeJob() for _ in range(job_count)]

    experiments = [FakeExperiment(1, 2), FakeExperiment(2, 0), FakeExperiment(3, 5)]

    result = AsyncMock()
    result.scalars.return_value.unique.return_value.all.return_value = experiments
    session.execute.return_value = result

    repo = ExperimentRepositoryAfter(session)
    summaries = await repo.list_summaries()

    assert [s.job_count for s in summaries] == [2, 0, 5]
    # selectinload issues exactly one additional query regardless of experiment count --
    # here the mock collapses to a single execute() call because relationship loading
    # is handled by the ORM's internal batching, not a manual loop.
    assert session.execute.await_count == 1
