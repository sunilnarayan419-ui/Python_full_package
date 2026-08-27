class UniversityLocalScope:
    def __init__(self, species: str) -> None:
        self.species = species

    def compute_growth_rate(self, height_start_cm: float, height_end_cm: float, days: int) -> float:
        # growth_delta and daily_rate are local to this method call only.
        growth_delta = height_end_cm - height_start_cm
        daily_rate = growth_delta / days if days > 0 else 0.0
        return daily_rate

    @staticmethod
    def run() -> None:
        plant = UniversityLocalScope("Zea mays")
        rate = plant.compute_growth_rate(height_start_cm=20.0, height_end_cm=80.0, days=30)
        print("University - daily growth rate:", rate)


class InterviewLocalScope:
    def __init__(self) -> None:
        self.experiment_log: list[str] = []

    def run_trial(self, trial_name: str, readings: list[float]) -> dict[str, float]:
        # 'total', 'count', and 'result' exist only within this call and cannot
        # leak into other trials, even if run_trial is called multiple times.
        total = 0.0
        count = 0
        for reading in readings:
            total += reading
            count += 1

        if count == 0:
            result = {"trial": trial_name, "average": 0.0, "count": 0.0}
        else:
            result = {"trial": trial_name, "average": total / count, "count": float(count)}

        self.experiment_log.append(trial_name)
        return result

    @staticmethod
    def run() -> None:
        lab = InterviewLocalScope()
        trial_one = lab.run_trial("Trial-1", [1.2, 1.4, 1.1])
        trial_two = lab.run_trial("Trial-2", [])
        print("Interview - trial one:", trial_one)
        print("Interview - trial two (empty):", trial_two)
        print("Interview - experiment log:", lab.experiment_log)


class IndustryLocalScope:
    """Computes normalized expression scores without relying on hidden state."""

    def __init__(self, dataset_name: str) -> None:
        self.dataset_name = dataset_name

    def normalize_expression_values(self, raw_values: list[float]) -> list[float]:
        # All intermediate values are local; the function returns results
        # explicitly instead of mutating instance or global state.
        if not raw_values:
            return []

        minimum_value = min(raw_values)
        maximum_value = max(raw_values)
        value_range = maximum_value - minimum_value

        if value_range == 0:
            return [0.0 for _ in raw_values]

        normalized_values = [
            (value - minimum_value) / value_range for value in raw_values
        ]
        return normalized_values

    @staticmethod
    def run() -> None:
        pipeline = IndustryLocalScope("RNA-Seq-Batch-7")
        normalized = pipeline.normalize_expression_values([2.1, 8.4, 5.0, 8.4, 0.9])
        print("Industry - normalized expression values:", normalized)

        constant_values = pipeline.normalize_expression_values([5.0, 5.0, 5.0])
        print("Industry - normalized constant values:", constant_values)


if __name__ == "__main__":
    UniversityLocalScope.run()
    InterviewLocalScope.run()
    IndustryLocalScope.run()
