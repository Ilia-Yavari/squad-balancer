import statistics
from dataclasses import dataclass, fields


@dataclass
class Player:
    name: str
    attack: int
    defense: int
    goalkeeping: int
    stamina: int

    @property
    def stats(self) -> dict[str, int]:
        return {f.name: getattr(self, f.name) for f in fields(self) if f.name != "name"}

    @property
    def overall(self) -> float:
        return statistics.mean(self.stats.values())

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError(f"Player name must be a string, got {self.name!r}")
        if not self.name.strip():
            raise ValueError("Player name must be non-empty")

        stats = self.stats
        for stat, value in stats.items():
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{stat} must be an integer, got {value!r}")
            if not (1 <= value <= 100):
                raise ValueError(f"{stat} must be between 1 and 100, got {value!r}")
