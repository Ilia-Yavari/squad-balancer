from dataclasses import dataclass
from squad_balancer.player import Player


@dataclass(frozen=True)
class Team:
    name: str
    players: tuple[Player, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Team name must be a non-empty string.")
        if not isinstance(self.players, tuple):
            raise TypeError("Players must be provided as a tuple.")

    @property
    def total_strength(self) -> float:
        return sum(p.overall for p in self.players)

    def __len__(self) -> int:
        return len(self.players)
