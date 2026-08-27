from __future__ import annotations

import numpy as np
from scipy.optimize import linprog


class AgriculturalResourceAllocator:
    """Optimizes crop planting allocation to maximize profit under resource constraints via linear programming."""

    def __init__(
        self,
        profit_per_hectare: np.ndarray,
        water_ml_per_hectare: np.ndarray,
        fertilizer_g_per_hectare: np.ndarray,
        labor_hours_per_hectare: np.ndarray,
        available_water_ml: float,
        available_fertilizer_g: float,
        available_labor_hours: float,
        max_hectares_per_crop: np.ndarray,
    ) -> None:
        self.profit_per_hectare: np.ndarray = np.asarray(profit_per_hectare, dtype=float)
        self.water_ml_per_hectare: np.ndarray = np.asarray(water_ml_per_hectare, dtype=float)
        self.fertilizer_g_per_hectare: np.ndarray = np.asarray(fertilizer_g_per_hectare, dtype=float)
        self.labor_hours_per_hectare: np.ndarray = np.asarray(labor_hours_per_hectare, dtype=float)
        self.available_water_ml: float = available_water_ml
        self.available_fertilizer_g: float = available_fertilizer_g
        self.available_labor_hours: float = available_labor_hours
        self.max_hectares_per_crop: np.ndarray = np.asarray(max_hectares_per_crop, dtype=float)
        self.n_crops: int = self.profit_per_hectare.shape[0]

    def _build_inequality_constraints(self) -> tuple[np.ndarray, np.ndarray]:
        constraint_matrix = np.vstack(
            [
                self.water_ml_per_hectare,
                self.fertilizer_g_per_hectare,
                self.labor_hours_per_hectare,
            ]
        )
        constraint_bounds = np.array(
            [self.available_water_ml, self.available_fertilizer_g, self.available_labor_hours]
        )
        return constraint_matrix, constraint_bounds

    def optimize_allocation(self) -> dict[str, np.ndarray | float | bool]:
        objective_coefficients = -self.profit_per_hectare
        constraint_matrix, constraint_bounds = self._build_inequality_constraints()
        variable_bounds = [(0.0, upper) for upper in self.max_hectares_per_crop]

        result = linprog(
            c=objective_coefficients,
            A_ub=constraint_matrix,
            b_ub=constraint_bounds,
            bounds=variable_bounds,
            method="highs",
        )

        if not result.success:
            raise RuntimeError(f"Linear programming solver failed: {result.message}")

        return {
            "success": bool(result.success),
            "hectares_allocated": result.x,
            "maximum_profit": float(-result.fun),
        }

    def check_feasibility(self, hectares_allocated: np.ndarray) -> dict[str, bool]:
        water_used = float(self.water_ml_per_hectare @ hectares_allocated)
        fertilizer_used = float(self.fertilizer_g_per_hectare @ hectares_allocated)
        labor_used = float(self.labor_hours_per_hectare @ hectares_allocated)
        return {
            "water_within_limit": water_used <= self.available_water_ml + 1e-6,
            "fertilizer_within_limit": fertilizer_used <= self.available_fertilizer_g + 1e-6,
            "labor_within_limit": labor_used <= self.available_labor_hours + 1e-6,
            "non_negative_allocation": bool(np.all(hectares_allocated >= -1e-8)),
        }

    @staticmethod
    def run() -> None:
        profit_per_hectare = np.array([1200.0, 950.0, 1400.0])
        water_ml_per_hectare = np.array([50000.0, 32000.0, 61000.0])
        fertilizer_g_per_hectare = np.array([8000.0, 6000.0, 9500.0])
        labor_hours_per_hectare = np.array([18.0, 14.0, 22.0])
        max_hectares_per_crop = np.array([12.0, 15.0, 10.0])

        allocator = AgriculturalResourceAllocator(
            profit_per_hectare=profit_per_hectare,
            water_ml_per_hectare=water_ml_per_hectare,
            fertilizer_g_per_hectare=fertilizer_g_per_hectare,
            labor_hours_per_hectare=labor_hours_per_hectare,
            available_water_ml=850000.0,
            available_fertilizer_g=140000.0,
            available_labor_hours=380.0,
            max_hectares_per_crop=max_hectares_per_crop,
        )

        allocation_result = allocator.optimize_allocation()
        print("Allocation result:", allocation_result)

        feasibility = allocator.check_feasibility(allocation_result["hectares_allocated"])
        print("Feasibility checks:", feasibility)


if __name__ == "__main__":
    AgriculturalResourceAllocator.run()
