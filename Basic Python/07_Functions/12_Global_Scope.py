total_samples_collected = 0


class UniversityGlobalScope:
    def __init__(self, species: str) -> None:
        self.species = species

    def collect_sample(self) -> int:
        global total_samples_collected
        total_samples_collected += 1
        return total_samples_collected

    @staticmethod
    def run() -> None:
        collector = UniversityGlobalScope("Arabidopsis thaliana")
        first_id = collector.collect_sample()
        second_id = collector.collect_sample()
        print("University - first sample id:", first_id)
        print("University - second sample id:", second_id)
        print("University - global total:", total_samples_collected)


active_experiment_count = 0


class InterviewGlobalScope:
    def __init__(self, experiment_name: str) -> None:
        self.experiment_name = experiment_name

    def start_experiment(self) -> int:
        global active_experiment_count
        active_experiment_count += 1
        return active_experiment_count

    def stop_experiment(self) -> int:
        global active_experiment_count
        if active_experiment_count > 0:
            active_experiment_count -= 1
        return active_experiment_count

    @staticmethod
    def run() -> None:
        trial_a = InterviewGlobalScope("Trial-A")
        trial_b = InterviewGlobalScope("Trial-B")

        print("Interview - after starting A:", trial_a.start_experiment())
        print("Interview - after starting B:", trial_b.start_experiment())
        print("Interview - after stopping A:", trial_a.stop_experiment())
        print("Interview - final active count:", active_experiment_count)


class IndustryGlobalScope:
    """
    Demonstrates why relying on module-level global state is discouraged in
    production code, and shows the preferred alternative: encapsulating
    shared counters as instance state inside a dedicated registry class.
    """

    def __init__(self) -> None:
        self._registered_sample_count = 0  # instance state, not global state

    def register_sample(self) -> int:
        self._registered_sample_count += 1
        return self._registered_sample_count

    @property
    def registered_sample_count(self) -> int:
        return self._registered_sample_count

    @staticmethod
    def run() -> None:
        registry_one = IndustryGlobalScope()
        registry_two = IndustryGlobalScope()

        registry_one.register_sample()
        registry_one.register_sample()
        registry_two.register_sample()

        print("Industry - registry one count:", registry_one.registered_sample_count)
        print("Industry - registry two count:", registry_two.registered_sample_count)
        print(
            "Industry - independent state confirms no shared global mutation "
            "between registries"
        )


if __name__ == "__main__":
    UniversityGlobalScope.run()
    InterviewGlobalScope.run()
    IndustryGlobalScope.run()
