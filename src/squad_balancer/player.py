import pytest
from dataclasses import dataclass


@dataclass
class Player:
    name: str
    attack: int
    defense: int
    goalkeeping: int
    stamina: int

    @property
    def overall(self) -> float:
        return sum((self.attack, self.defense, self.goalkeeping, self.stamina)) / 4

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Player name must be a non-empty string.")

        stats = {k: v for k, v in vars(self).items() if k != "name"}
        for k, v in stats.items():
            if isinstance(v, bool) or not isinstance(v, int) or not (1 <= v <= 100):
                raise ValueError(f"{k} must be an integer between 1 and 100, got {v}")