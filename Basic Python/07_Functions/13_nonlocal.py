class UniversityNonlocal:
    def __init__(self, species: str) -> None:
        self.species = species

    def make_sample_counter(self):
        sample_count = 0  # enclosing scope variable

        def record_sample() -> int:
            nonlocal sample_count
            sample_count += 1
            return sample_count

        return record_sample

    @staticmethod
    def run() -> None:
        plant = UniversityNonlocal("Zea mays")
        counter = plant.make_sample_counter()
        print("University - first call:", counter())
        print("University - second call:", counter())
        print("University - third call:", counter())


class InterviewNonlocal:
    def __init__(self, experiment_name: str) -> None:
        self.experiment_name = experiment_name

    def make_running_average(self):
        total = 0.0
        count = 0

        def add_reading(value: float) -> float:
            nonlocal total, count
            total += value
            count += 1
            return total / count

        return add_reading

    @staticmethod
    def run() -> None:
        lab = InterviewNonlocal("pH-Monitoring")
        running_average = lab.make_running_average()
        print("Interview - average after 1 reading:", running_average(6.8))
        print("Interview - average after 2 readings:", running_average(7.2))
        print("Interview - average after 3 readings:", running_average(7.0))

        independent_average = lab.make_running_average()
        print("Interview - independent tracker:", independent_average(5.0))


global_experiment_registry_count = 0


class IndustryNonlocal:
    """
    Demonstrates the practical difference between 'global' and 'nonlocal' by
    building an experiment counter factory. Each closure maintains its own
    isolated count via 'nonlocal', while a separate module-level counter
    demonstrates 'global' mutation for comparison.
    """

    def __init__(self, lab_name: str) -> None:
        self.lab_name = lab_name

    def make_experiment_id_generator(self, prefix: str):
        sequence_number = 0  # private to this closure via nonlocal

        def next_id() -> str:
            nonlocal sequence_number
            sequence_number += 1
            self._increment_global_registry()
            return f"{prefix}-{sequence_number:03d}"

        return next_id

    @staticmethod
    def _increment_global_registry() -> None:
        global global_experiment_registry_count
        global_experiment_registry_count += 1

    @staticmethod
    def run() -> None:
        lab = IndustryNonlocal("Central Genomics Lab")
        soil_experiment_ids = lab.make_experiment_id_generator("SOIL")
        water_experiment_ids = lab.make_experiment_id_generator("WATER")

        print("Industry - soil id 1:", soil_experiment_ids())
        print("Industry - soil id 2:", soil_experiment_ids())
        print("Industry - water id 1:", water_experiment_ids())
        print(
            "Industry - global registry total (via 'global'):",
            global_experiment_registry_count,
        )


if __name__ == "__main__":
    UniversityNonlocal.run()
    InterviewNonlocal.run()
    IndustryNonlocal.run()
