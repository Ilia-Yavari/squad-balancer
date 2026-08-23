from itertools import combinations
from typing import Sequence

from squad_balancer.player import Player
from squad_balancer.team import Team


def balance_teams(
    players: Sequence[Player],
    team_a_name: str = "Team A",
    team_b_name: str = "Team B",
) -> tuple[Team, Team]:
    if len(players) < 2:
        raise ValueError("At least 2 players are required to form teams")

    total_players = len(players)
    team_a_size = total_players // 2

    best_diff = float("inf")
    best_teams: tuple[Team, Team] | None = None

    for a_indices in combinations(range(total_players), team_a_size):
        team_a_players = tuple(players[i] for i in a_indices)
        team_b_players = tuple(players[i] for i in range(total_players) if i not in a_indices)

        team_a = Team(team_a_name, team_a_players)
        team_b = Team(team_b_name, team_b_players)

        diff = abs(team_a.total_strength - team_b.total_strength)

        if diff < best_diff:
            best_diff = diff
            best_teams = (team_a, team_b)

        if diff == 0:
            break

    if best_teams is None:
        raise RuntimeError("Failed to balance teams")

    return best_teams
