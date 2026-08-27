"""A professional weather-application architecture.

Provider abstraction -> WeatherService -> WeatherModel -> CLI. Ships
with a deterministic MockWeatherProvider for offline demonstration and
testing; a real provider can be plugged in without touching the
service or CLI layers. No API keys are embedded; a real provider would
read credentials from an environment variable.
"""

from __future__ import annotations

import logging
import os
import time
import zlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

WEATHER_API_KEY_ENV_VAR = "WEATHER_API_KEY"
CACHE_TTL_SECONDS = 300


class WeatherError(Exception):
    """Base exception for weather-related failures."""


class LocationNotFoundError(WeatherError):
    """Raised when the requested location cannot be resolved."""


class WeatherServiceTimeoutError(WeatherError):
    """Raised when the weather provider does not respond in time."""


class ProviderUnavailableError(WeatherError):
    """Raised when a provider cannot serve a request (e.g. missing credentials)."""


class Condition(Enum):
    CLEAR = "Clear"
    CLOUDY = "Cloudy"
    RAINY = "Rainy"
    STORMY = "Stormy"
    SNOWY = "Snowy"


@dataclass(slots=True, frozen=True)
class WeatherReading:
    """A structured snapshot of weather conditions for a location."""

    location: str
    temperature_celsius: float
    humidity_percent: float
    wind_kph: float
    condition: Condition

    def summary(self) -> str:
        return (
            f"{self.location}: {self.temperature_celsius:.1f}C, "
            f"{self.condition.value}, humidity {self.humidity_percent:.0f}%, "
            f"wind {self.wind_kph:.1f} kph"
        )


class WeatherProvider(ABC):
    """Abstract interface any weather data source must implement."""

    @abstractmethod
    def fetch(self, location: str, timeout_seconds: float) -> WeatherReading:
        """Fetch current conditions for `location` or raise a WeatherError."""


class MockWeatherProvider(WeatherProvider):
    """A deterministic, offline weather provider for demos and tests.

    Values are derived deterministically from the location name so
    repeated calls for the same location are reproducible without
    requiring network access or an API key.
    """

    def fetch(self, location: str, timeout_seconds: float) -> WeatherReading:
        normalized = location.strip()
        if not normalized:
            raise LocationNotFoundError("Location cannot be empty.")

        seed = zlib.crc32(normalized.lower().encode("utf-8"))
        temperature = -5 + (seed % 400) / 10.0
        humidity = 20 + (seed % 700) / 10.0
        wind = (seed % 500) / 10.0
        condition = list(Condition)[seed % len(Condition)]

        return WeatherReading(
            location=normalized,
            temperature_celsius=round(temperature, 1),
            humidity_percent=round(min(humidity, 100.0), 1),
            wind_kph=round(wind, 1),
            condition=condition,
        )


class LiveWeatherProvider(WeatherProvider):
    """Placeholder for a real HTTP-backed provider.

    A production implementation would call an external weather API
    using the API key from the WEATHER_API_KEY environment variable
    and a bounded request timeout. It is not implemented here to avoid
    embedding real network calls or credentials in this exercise.
    """

    def __init__(self) -> None:
        self._api_key = os.environ.get(WEATHER_API_KEY_ENV_VAR)
        if not self._api_key:
            raise ProviderUnavailableError(
                f"Set the {WEATHER_API_KEY_ENV_VAR} environment variable to use the live provider."
            )

    def fetch(self, location: str, timeout_seconds: float) -> WeatherReading:
        raise ProviderUnavailableError(
            "Live provider is not implemented in this offline exercise. "
            "Use MockWeatherProvider, or implement an HTTP client here."
        )


class WeatherCache:
    """A simple time-based in-memory cache for weather readings."""

    def __init__(self, ttl_seconds: float = CACHE_TTL_SECONDS) -> None:
        self._ttl_seconds = ttl_seconds
        self._store: dict[str, tuple[float, WeatherReading]] = {}

    def get(self, location: str) -> WeatherReading | None:
        key = location.strip().lower()
        entry = self._store.get(key)
        if entry is None:
            return None
        timestamp, reading = entry
        if time.monotonic() - timestamp > self._ttl_seconds:
            del self._store[key]
            return None
        return reading

    def set(self, location: str, reading: WeatherReading) -> None:
        key = location.strip().lower()
        self._store[key] = (time.monotonic(), reading)


class WeatherService:
    """Business logic layer that mediates between the CLI and a provider."""

    def __init__(self, provider: WeatherProvider, cache: WeatherCache | None = None,
                 timeout_seconds: float = 5.0) -> None:
        self._provider = provider
        self._cache = cache or WeatherCache()
        self._timeout_seconds = timeout_seconds

    def get_current_weather(self, location: str, use_cache: bool = True) -> WeatherReading:
        if use_cache:
            cached = self._cache.get(location)
            if cached is not None:
                return cached

        reading = self._provider.fetch(location, self._timeout_seconds)
        self._cache.set(location, reading)
        return reading


def main() -> None:
    """Entry point for the interactive weather CLI."""
    print("=== Weather App (using offline mock provider) ===")
    service = WeatherService(MockWeatherProvider())

    while True:
        location = input("\nEnter a location (or 'quit' to exit): ").strip()
        if location.lower() == "quit":
            print("Goodbye.")
            break

        try:
            reading = service.get_current_weather(location)
            print(reading.summary())
        except WeatherError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
