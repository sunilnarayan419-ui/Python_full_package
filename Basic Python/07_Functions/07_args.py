class UniversityArgs:
    def __init__(self, plant_species: str) -> None:
        self.plant_species = plant_species

    def total_leaf_area(self, *leaf_areas_cm2: float) -> float:
        return sum(leaf_areas_cm2)

    def average_leaf_area(self, *leaf_areas_cm2: float) -> float:
        if not leaf_areas_cm2:
            return 0.0
        return sum(leaf_areas_cm2) / len(leaf_areas_cm2)

    @staticmethod
    def run() -> None:
        plant = UniversityArgs("Ficus benjamina")
        total = plant.total_leaf_area(12.4, 15.1, 9.8, 20.0)
        average = plant.average_leaf_area(12.4, 15.1, 9.8, 20.0)
        print("University - total leaf area:", total)
        print("University - average leaf area:", average)


class InterviewArgs:
    def __init__(self, experiment_name: str) -> None:
        self.experiment_name = experiment_name

    def aggregate_measurements(self, *measurements: float) -> dict[str, float]:
        if not measurements:
            return {"count": 0, "sum": 0.0, "min": 0.0, "max": 0.0}
        return {
            "count": len(measurements),
            "sum": sum(measurements),
            "min": min(measurements),
            "max": max(measurements),
        }

    def combine_with_named_arg(self, label: str, *measurements: float) -> str:
        stats = self.aggregate_measurements(*measurements)
        return f"{label}: {stats}"

    @staticmethod
    def run() -> None:
        experiment = InterviewArgs("Root-Length-Trial")
        stats = experiment.aggregate_measurements(3.2, 4.1, 2.9, 5.0)
        print("Interview - stats:", stats)

        empty_stats = experiment.aggregate_measurements()
        print("Interview - empty stats:", empty_stats)

        combined = experiment.combine_with_named_arg("Root-Length-Trial", 3.2, 4.1, 2.9)
        print("Interview - combined:", combined)


class IndustryArgs:
    """Aggregates readings from an arbitrary number of sensor sources."""

    def __init__(self, pipeline_name: str) -> None:
        if not pipeline_name.strip():
            raise ValueError("pipeline_name must not be empty")
        self.pipeline_name = pipeline_name

    def merge_sensor_readings(self, *readings: dict[str, float]) -> dict[str, object]:
        if not readings:
            raise ValueError("At least one sensor reading is required")
        values = [reading["value"] for reading in readings]
        return {
            "pipeline": self.pipeline_name,
            "sample_size": len(values),
            "mean": sum(values) / len(values),
            "spread": max(values) - min(values),
        }

    @staticmethod
    def run() -> None:
        pipeline = IndustryArgs("Soil-Moisture-Network")
        readings = (
            {"sensor_id": "S1", "value": 22.5},
            {"sensor_id": "S2", "value": 24.1},
            {"sensor_id": "S3", "value": 21.9},
        )
        merged = pipeline.merge_sensor_readings(*readings)
        print("Industry - merged readings:", merged)

        try:
            pipeline.merge_sensor_readings()
        except ValueError as error:
            print("Industry - empty reading guard:", error)


if __name__ == "__main__":
    UniversityArgs.run()
    InterviewArgs.run()
    IndustryArgs.run()
