"""Production-quality mocking example: isolating an experiment service
from its external dependencies using unittest.mock.
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Protocol
from unittest.mock import MagicMock, Mock, call, patch


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    experiment_id: str
    mean_expression: float
    sample_count: int


class SampleRepository(Protocol):
    """External boundary: persistent storage of raw sample records."""

    def fetch_samples(self, experiment_id: str) -> list[dict[str, float]]: ...


class ScientificDataProvider(Protocol):
    """External boundary: third-party service normalizing raw readings."""

    def normalize(self, raw_samples: list[dict[str, float]]) -> list[float]: ...


class ReportPublisher(Protocol):
    """External boundary: publishes finalized results to a reporting system."""

    def publish(self, result: ExperimentResult) -> None: ...


class ExperimentService:
    """Coordinates sample retrieval, normalization, and result publication.

    Dependencies are injected so external systems (database, third-party
    normalization API, reporting pipeline) can be substituted with test
    doubles at their natural architectural boundary.
    """

    def __init__(
        self,
        repository: SampleRepository,
        data_provider: ScientificDataProvider,
        publisher: ReportPublisher,
    ) -> None:
        self._repository = repository
        self._data_provider = data_provider
        self._publisher = publisher

    def run_experiment(self, experiment_id: str) -> ExperimentResult:
        raw_samples = self._repository.fetch_samples(experiment_id)
        if not raw_samples:
            raise ValueError(f"no samples found for experiment {experiment_id}")

        normalized = self._data_provider.normalize(raw_samples)
        mean_expression = sum(normalized) / len(normalized)

        result = ExperimentResult(
            experiment_id=experiment_id,
            mean_expression=mean_expression,
            sample_count=len(normalized),
        )
        self._publisher.publish(result)
        return result


class TestExperimentServiceBehavior(unittest.TestCase):
    """Tests ExperimentService's own orchestration logic, not its dependencies."""

    def setUp(self) -> None:
        self.repository = Mock(spec=SampleRepository)
        self.data_provider = Mock(spec=ScientificDataProvider)
        self.publisher = Mock(spec=ReportPublisher)
        self.service = ExperimentService(
            self.repository, self.data_provider, self.publisher
        )

    def test_run_experiment_computes_mean_and_publishes(self) -> None:
        self.repository.fetch_samples.return_value = [
            {"reading": 1.0},
            {"reading": 2.0},
            {"reading": 3.0},
        ]
        self.data_provider.normalize.return_value = [10.0, 20.0, 30.0]

        result = self.service.run_experiment("EXP-001")

        self.assertEqual(result.experiment_id, "EXP-001")
        self.assertAlmostEqual(result.mean_expression, 20.0, places=6)
        self.assertEqual(result.sample_count, 3)

        # Verify the service called its collaborators correctly, not their
        # internals -- that is the responsibility of each dependency's own
        # test suite.
        self.repository.fetch_samples.assert_called_once_with("EXP-001")
        self.data_provider.normalize.assert_called_once_with(
            self.repository.fetch_samples.return_value
        )
        self.publisher.publish.assert_called_once_with(result)

    def test_run_experiment_raises_when_no_samples(self) -> None:
        self.repository.fetch_samples.return_value = []

        with self.assertRaises(ValueError):
            self.service.run_experiment("EXP-002")

        # Empty input must short-circuit before touching downstream systems.
        self.data_provider.normalize.assert_not_called()
        self.publisher.publish.assert_not_called()

    def test_run_experiment_propagates_provider_failure_without_publishing(self) -> None:
        self.repository.fetch_samples.return_value = [{"reading": 1.0}]
        self.data_provider.normalize.side_effect = RuntimeError("normalization service down")

        with self.assertRaises(RuntimeError):
            self.service.run_experiment("EXP-003")

        self.publisher.publish.assert_not_called()

    def test_run_experiment_call_order(self) -> None:
        manager = Mock()
        manager.attach_mock(self.repository.fetch_samples, "fetch_samples")
        manager.attach_mock(self.data_provider.normalize, "normalize")
        manager.attach_mock(self.publisher.publish, "publish")

        self.repository.fetch_samples.return_value = [{"reading": 1.0}]
        self.data_provider.normalize.return_value = [5.0]

        self.service.run_experiment("EXP-004")

        expected_calls = [
            call.fetch_samples("EXP-004"),
            call.normalize([{"reading": 1.0}]),
            call.publish(manager.publish.call_args.args[0]),
        ]
        self.assertEqual(manager.mock_calls, expected_calls)


class TestExperimentServiceWithPatchedModuleLevelDependency(unittest.TestCase):
    """Demonstrates patch()/patch.object() where a dependency is resolved
    from module or class attributes rather than passed explicitly.
    """

    def test_patch_object_replaces_bound_method_for_duration_of_test(self) -> None:
        repository = Mock(spec=SampleRepository)
        data_provider = Mock(spec=ScientificDataProvider)
        publisher = Mock(spec=ReportPublisher)
        service = ExperimentService(repository, data_provider, publisher)

        repository.fetch_samples.return_value = [{"reading": 1.0}]
        data_provider.normalize.return_value = [42.0]

        # patch.object demonstrates temporarily overriding a collaborator's
        # method without altering the injected instance's identity.
        with patch.object(
            publisher, "publish", new=MagicMock(name="publish_override")
        ) as publish_mock:
            service.run_experiment("EXP-005")
            publish_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
