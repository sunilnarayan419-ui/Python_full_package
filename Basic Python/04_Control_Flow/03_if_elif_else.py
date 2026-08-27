"""if/elif/else multi-category classification."""


class HeightClassifier:
    def __init__(self, height_cm: float) -> None:
        self.height_cm = height_cm

    def category(self) -> str:
        if self.height_cm < 20:
            return "short"
        elif self.height_cm < 50:
            return "medium"
        else:
            return "tall"


class ExpressionLevel:
    def __init__(self, value: float) -> None:
        self.value = value

    def level(self) -> str:
        if self.value < 1.0:
            return "low"
        elif self.value < 5.0:
            return "normal"
        elif self.value < 20.0:
            return "high"
        else:
            return "very_high"


class PlantStressCategory:
    def __init__(self, water_pct: float, temperature_c: float) -> None:
        self.water_pct = water_pct
        self.temperature_c = temperature_c

    def category(self) -> str:
        if self.water_pct < 30:
            return "drought_stress"
        elif self.water_pct > 80 and self.temperature_c > 30:
            return "heat_humidity_stress"
        elif self.temperature_c < 5:
            return "cold_stress"
        else:
            return "normal"


if __name__ == "__main__":
    print(HeightClassifier(45.0).category())

    print(ExpressionLevel(8.0).level())

    print(PlantStressCategory(water_pct=85, temperature_c=32).category())
