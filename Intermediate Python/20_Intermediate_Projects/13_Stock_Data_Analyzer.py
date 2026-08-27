from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

TRADING_DAYS_PER_YEAR = 252


class MarketDataError(Exception):
    """Raised when market data fails validation."""


@dataclass(frozen=True, slots=True)
class PerformanceSummary:
    total_return_pct: float
    annualized_volatility_pct: float
    max_drawdown_pct: float
    sharpe_ratio: float
    average_daily_return_pct: float


class MarketDataValidator:
    """Validates a price series before analysis."""

    def validate(self, prices: pd.Series) -> None:
        if prices.empty:
            raise MarketDataError("Price series is empty.")
        if (prices <= 0).any():
            raise MarketDataError("Price series contains non-positive values.")
        if prices.isna().any():
            raise MarketDataError("Price series contains missing values.")


class ReturnsCalculator:
    """Computes return series from a price series."""

    def daily_returns(self, prices: pd.Series) -> pd.Series:
        return prices.pct_change().dropna()

    def cumulative_returns(self, daily_returns: pd.Series) -> pd.Series:
        return (1 + daily_returns).cumprod() - 1


class MovingAverageCalculator:
    """Computes rolling moving averages for a price series."""

    def simple_moving_average(self, prices: pd.Series, window: int) -> pd.Series:
        if window <= 0:
            raise ValueError("window must be positive.")
        return prices.rolling(window=window, min_periods=window).mean()


class RiskCalculator:
    """Computes volatility and drawdown statistics."""

    def annualized_volatility(self, daily_returns: pd.Series) -> float:
        return float(daily_returns.std(ddof=1) * np.sqrt(TRADING_DAYS_PER_YEAR))

    def max_drawdown(self, prices: pd.Series) -> float:
        running_max = prices.cummax()
        drawdown = (prices - running_max) / running_max
        return float(drawdown.min())

    def sharpe_ratio(self, daily_returns: pd.Series, risk_free_rate_annual: float = 0.0) -> float:
        excess_daily_rf = risk_free_rate_annual / TRADING_DAYS_PER_YEAR
        excess_returns = daily_returns - excess_daily_rf
        std = excess_returns.std(ddof=1)
        if std == 0:
            return 0.0
        return float((excess_returns.mean() / std) * np.sqrt(TRADING_DAYS_PER_YEAR))


class StockDataAnalyzer:
    """Coordinates validation, return computation, and risk analysis for a price series."""

    def __init__(
        self,
        validator: MarketDataValidator | None = None,
        returns_calculator: ReturnsCalculator | None = None,
        moving_average_calculator: MovingAverageCalculator | None = None,
        risk_calculator: RiskCalculator | None = None,
    ) -> None:
        self._validator = validator or MarketDataValidator()
        self._returns_calculator = returns_calculator or ReturnsCalculator()
        self._moving_average_calculator = moving_average_calculator or MovingAverageCalculator()
        self._risk_calculator = risk_calculator or RiskCalculator()

    def build_summary(self, prices: pd.Series) -> PerformanceSummary:
        self._validator.validate(prices)
        daily_returns = self._returns_calculator.daily_returns(prices)

        total_return_pct = float((prices.iloc[-1] / prices.iloc[0] - 1) * 100)
        volatility_pct = self._risk_calculator.annualized_volatility(daily_returns) * 100
        max_drawdown_pct = self._risk_calculator.max_drawdown(prices) * 100
        sharpe = self._risk_calculator.sharpe_ratio(daily_returns)
        avg_daily_return_pct = float(daily_returns.mean() * 100)

        return PerformanceSummary(
            total_return_pct=round(total_return_pct, 2),
            annualized_volatility_pct=round(volatility_pct, 2),
            max_drawdown_pct=round(max_drawdown_pct, 2),
            sharpe_ratio=round(sharpe, 3),
            average_daily_return_pct=round(avg_daily_return_pct, 4),
        )

    def moving_averages(self, prices: pd.Series, short_window: int = 20, long_window: int = 50) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "price": prices,
                f"sma_{short_window}": self._moving_average_calculator.simple_moving_average(prices, short_window),
                f"sma_{long_window}": self._moving_average_calculator.simple_moving_average(prices, long_window),
            }
        )


def _build_sample_price_series() -> pd.Series:
    """Builds a deterministic synthetic price series for demonstration purposes."""
    rng = np.random.default_rng(42)
    n_days = 252
    daily_log_returns = rng.normal(loc=0.0003, scale=0.015, size=n_days)
    prices = 100 * np.exp(np.cumsum(daily_log_returns))
    dates = pd.date_range(end=date.today(), periods=n_days, freq="B")
    return pd.Series(prices.round(2), index=dates, name="close_price")


def run() -> PerformanceSummary:
    """Runs the stock data analyzer against deterministic synthetic price data."""
    prices = _build_sample_price_series()
    analyzer = StockDataAnalyzer()

    summary = analyzer.build_summary(prices)
    logger.info("Total return: %.2f%%", summary.total_return_pct)
    logger.info("Annualized volatility: %.2f%%", summary.annualized_volatility_pct)
    logger.info("Max drawdown: %.2f%%", summary.max_drawdown_pct)
    logger.info("Sharpe ratio: %.3f", summary.sharpe_ratio)

    moving_averages = analyzer.moving_averages(prices)
    logger.info("Latest moving averages:\n%s", moving_averages.tail(3).to_string())

    return summary


if __name__ == "__main__":
    run()
