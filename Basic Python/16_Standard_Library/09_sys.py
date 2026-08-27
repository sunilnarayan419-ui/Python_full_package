"""Demonstrates the sys module for runtime inspection and CLI-style utilities."""

import sys


class UniversitySys:
    """Introduces inspecting the Python runtime environment."""

    def get_python_version(self) -> str:
        return sys.version.split()[0]

    def get_platform(self) -> str:
        return sys.platform

    @staticmethod
    def run() -> None:
        inspector = UniversitySys()
        print(f"Python version: {inspector.get_python_version()}")
        print(f"Platform identifier: {inspector.get_platform()}")


class InterviewSys:
    """Solves a command-line argument parsing problem with sensible defaults."""

    def parse_sample_count(self, argv: list[str], default: int = 5) -> int:
        """Parse a sample count from argv, falling back to a default.

        Raises ValueError for a non-numeric argument, giving the caller a clear
        signal instead of an unhandled ValueError from int() deep in the stack.
        """
        if len(argv) < 2:
            return default
        try:
            count = int(argv[1])
        except ValueError as error:
            raise ValueError(f"Invalid sample count argument: '{argv[1]}'") from error

        if count <= 0:
            raise ValueError("Sample count must be positive.")
        return count

    @staticmethod
    def run() -> None:
        solver = InterviewSys()

        # Test case 1: no arguments provided, defaults are used
        count = solver.parse_sample_count(argv=["script.py"])
        print(f"Sample count (default): {count}")

        # Test case 2: valid explicit argument
        count = solver.parse_sample_count(argv=["script.py", "12"])
        print(f"Sample count (explicit): {count}")

        # Test case 3: edge case, invalid argument
        try:
            solver.parse_sample_count(argv=["script.py", "not_a_number"])
        except ValueError as error:
            print(f"Handled invalid argument: {error}")


class IndustrySys:
    """Small CLI-style scientific utility built on sys.argv and sys.stderr."""

    def __init__(self, argv: list[str]) -> None:
        self.argv = argv

    def get_option(self, flag: str, default: str) -> str:
        """Retrieve a '--flag value' style option from argv, or return the default."""
        if flag in self.argv:
            index = self.argv.index(flag)
            if index + 1 < len(self.argv):
                return self.argv[index + 1]
        return default

    def run_pipeline(self) -> dict[str, str]:
        """Run a minimal scientific processing pipeline configured via CLI-style flags."""
        input_format = self.get_option("--format", default="csv")
        threshold = self.get_option("--threshold", default="0.5")

        try:
            threshold_value = float(threshold)
        except ValueError:
            print(f"Invalid threshold '{threshold}', using default 0.5", file=sys.stderr)
            threshold_value = 0.5

        return {"input_format": input_format, "threshold": f"{threshold_value:.2f}"}

    @staticmethod
    def run() -> None:
        # Safe deterministic defaults are used so the module runs without
        # requiring real command-line arguments.
        demo_argv = ["genomics_tool.py", "--format", "fasta", "--threshold", "0.75"]
        utility = IndustrySys(demo_argv)

        configuration = utility.run_pipeline()
        print(f"Pipeline configuration: {configuration}")


if __name__ == "__main__":
    UniversitySys.run()
    InterviewSys.run()
    IndustrySys.run()
