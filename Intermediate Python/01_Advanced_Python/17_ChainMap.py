from __future__ import annotations

from collections import ChainMap
from typing import Any


class UniversityChainMap:
    """Demonstrates collections.ChainMap for layering two dictionaries
    without merging them into a new dict."""

    @staticmethod
    def run() -> None:
        defaults = {"incubation_temp_c": 25, "light_hours": 12}
        overrides = {"light_hours": 16}

        config = ChainMap(overrides, defaults)
        print(f"incubation_temp_c={config['incubation_temp_c']}")
        print(f"light_hours={config['light_hours']}")
        print(dict(config))


class InterviewChainMap:
    """Demonstrates ChainMap for layered configuration resolution with
    lookup precedence, plus the distinction between mutating the top layer
    versus the underlying maps."""

    @staticmethod
    def run() -> None:
        lab_defaults = {"ph_target": 7.0, "shaking_rpm": 150, "duration_hours": 24}
        protocol_settings = {"shaking_rpm": 200}
        experiment_overrides: dict[str, Any] = {}

        config = ChainMap(experiment_overrides, protocol_settings, lab_defaults)
        print(f"before override: shaking_rpm={config['shaking_rpm']}")

        config["duration_hours"] = 48  # writes go to the first mapping only
        print(f"experiment_overrides after write: {experiment_overrides}")
        print(f"protocol_settings unchanged: {protocol_settings}")
        print(f"resolved duration_hours={config['duration_hours']}")

        print(f"all keys visible: {sorted(config.keys())}")


class IndustryChainMap:
    """Demonstrates ChainMap as the backbone of a layered configuration
    service for a laboratory information system: global defaults,
    per-instrument calibration profiles, and per-run overrides, with a
    clean API and validation of override keys."""

    class ExperimentConfig:
        def __init__(
            self,
            global_defaults: dict[str, Any],
            instrument_profile: dict[str, Any],
        ) -> None:
            self._run_overrides: dict[str, Any] = {}
            self._chain: ChainMap[str, Any] = ChainMap(
                self._run_overrides, instrument_profile, global_defaults
            )
            self._known_keys = set(global_defaults) | set(instrument_profile)

        def set_override(self, key: str, value: Any) -> None:
            if key not in self._known_keys:
                raise KeyError(f"unknown configuration key: {key}")
            self._run_overrides[key] = value

        def get(self, key: str) -> Any:
            if key not in self._chain:
                raise KeyError(f"unknown configuration key: {key}")
            return self._chain[key]

        def resolved(self) -> dict[str, Any]:
            return dict(self._chain)

        def source_of(self, key: str) -> str:
            for label, mapping in (
                ("run_override", self._run_overrides),
                ("instrument_profile", self._chain.maps[1]),
                ("global_default", self._chain.maps[2]),
            ):
                if key in mapping:
                    return label
            raise KeyError(f"unknown configuration key: {key}")

    @staticmethod
    def run() -> None:
        global_defaults = {"sampling_rate_hz": 10, "gain": 1.0, "auto_calibrate": True}
        instrument_profile = {"gain": 2.5}

        config = IndustryChainMap.ExperimentConfig(global_defaults, instrument_profile)
        print(f"gain resolved from: {config.source_of('gain')} -> {config.get('gain')}")

        config.set_override("sampling_rate_hz", 20)
        print(f"sampling_rate_hz resolved from: {config.source_of('sampling_rate_hz')} -> {config.get('sampling_rate_hz')}")
        print(f"full resolved config: {config.resolved()}")

        try:
            config.set_override("unsupported_key", 5)
        except KeyError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityChainMap.run()
    InterviewChainMap.run()
    IndustryChainMap.run()
