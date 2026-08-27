"""Demonstrates the os module for scientific project environment inspection."""

import os


class UniversityOs:
    """Introduces basic OS interaction: current directory and platform info."""

    def get_current_working_directory(self) -> str:
        return os.getcwd()

    def get_platform_name(self) -> str:
        return os.name

    @staticmethod
    def run() -> None:
        inspector = UniversityOs()
        print(f"Current working directory: {inspector.get_current_working_directory()}")
        print(f"OS name identifier: {inspector.get_platform_name()}")


class InterviewOs:
    """Solves an environment-variable configuration problem with fallbacks."""

    def resolve_dataset_directory(self, env_var_name: str, default: str) -> str:
        """Resolve a dataset directory from an environment variable, or fall back.

        Falling back to a default rather than raising keeps the utility usable
        in environments (like CI or a fresh laptop) where the variable is unset.
        """
        return os.environ.get(env_var_name, default)

    def list_env_vars_with_prefix(self, prefix: str) -> dict[str, str]:
        """Return environment variables whose name starts with the given prefix.

        Returns an empty dict rather than raising when no variables match,
        since an empty configuration namespace is a valid, expected state.
        """
        return {key: value for key, value in os.environ.items() if key.startswith(prefix)}

    @staticmethod
    def run() -> None:
        solver = InterviewOs()

        # Test case 1: variable likely unset, exercising the fallback path
        dataset_dir = solver.resolve_dataset_directory("LAB_DATASET_DIR", default="./data")
        print(f"Resolved dataset directory: {dataset_dir}")

        # Test case 2: no matches, exercising the empty-result path
        lab_vars = solver.list_env_vars_with_prefix("LAB_EXPERIMENT_")
        print(f"Matching LAB_EXPERIMENT_ variables: {lab_vars}")


class IndustryOs:
    """Environment-aware configuration loader for a scientific application."""

    def __init__(self, prefix: str = "SCI_APP_") -> None:
        self.prefix = prefix

    def load_configuration(self, defaults: dict[str, str]) -> dict[str, str]:
        """Build a configuration dict, letting prefixed environment variables
        override sensible defaults without ever hard-coding user-specific paths.
        """
        configuration = dict(defaults)
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                config_key = key[len(self.prefix):].lower()
                configuration[config_key] = value
        return configuration

    def describe_runtime_environment(self) -> dict[str, str]:
        """Summarize non-sensitive runtime environment details for diagnostics."""
        return {
            "platform": os.name,
            "cpu_count": str(os.cpu_count()),
            "working_directory": os.getcwd(),
        }

    @staticmethod
    def run() -> None:
        loader = IndustryOs(prefix="SCI_APP_")

        defaults = {"results_dir": "./results", "log_level": "INFO"}
        configuration = loader.load_configuration(defaults)
        print(f"Application configuration: {configuration}")

        runtime_info = loader.describe_runtime_environment()
        print(f"Runtime environment: {runtime_info}")


if __name__ == "__main__":
    UniversityOs.run()
    InterviewOs.run()
    IndustryOs.run()
