from dataclasses import dataclass
from squad_balancer.player import Player


@dataclass(frozen=True)
class Team:
    name: str
    players: tuple[Player, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError(f"Team name must be a string, got {self.name!r}")
        if not self.name.strip():
            raise ValueError("Team name must be non-empty")
        if not isinstance(self.players, tuple):
            raise TypeError("Players must be provided as a tuple")
        for item in self.players:
            if not isinstance(item, Player):
                raise TypeError(f"Players must contain only Player instances, got {item!r}")

    @property
    def total_strength(self) -> float:
        return sum(p.overall for p in self.players)

    def __len__(self) -> int:
        return len(self.players)
