"""Clinical-trial summary construction with intentionally complex
signatures, nested structures, and long call chains to demonstrate
where Black's deterministic formatting matters most.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(slots=True)
class ClinicalTrialSummary:
    trial_id: str
    enrolled_patients: int
    completed_patients: int
    adverse_events: dict[str, int] = field(default_factory=dict)
    secondary_endpoints: list[tuple[str, float, float]] = field(default_factory=list)

    @property
    def completion_rate(self) -> float:
        if self.enrolled_patients == 0:
            return 0.0
        return self.completed_patients / self.enrolled_patients


def build_summary(
    trial_id: str,
    enrolled_patients: int,
    completed_patients: int,
    adverse_event_counts: dict[str, int] | None = None,
    secondary_endpoint_results: list[tuple[str, float, float]] | None = None,
    *,
    endpoint_transform: (
        Callable[[tuple[str, float, float]], tuple[str, float, float]] | None
    ) = None,
) -> ClinicalTrialSummary:
    endpoints = secondary_endpoint_results if secondary_endpoint_results is not None else []
    transformed_endpoints = (
        [endpoint_transform(endpoint) for endpoint in endpoints]
        if endpoint_transform is not None
        else endpoints
    )
    return ClinicalTrialSummary(
        trial_id=trial_id,
        enrolled_patients=enrolled_patients,
        completed_patients=completed_patients,
        adverse_events=adverse_event_counts if adverse_event_counts is not None else {},
        secondary_endpoints=transformed_endpoints,
    )
