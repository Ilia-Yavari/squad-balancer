import pytest

from squad_balancer.balancer import balance_teams
from squad_balancer.player import Player


def test_players_less_than_two_raises_value_error():
    with pytest.raises(ValueError, match="At least 2 players are required to form teams."):
        balance_teams([Player("John Doe", 76, 58, 82, 30)])


def test_balance_teams():
    players = [
        Player("John Doe", 76, 58, 82, 30),  # overall = 61.5
        Player("Jane Doe", 76, 63, 82, 30),  # overall = 62.75
        Player("J. Doe", 76, 58, 74, 82),  # overall = 72.5
        Player("JD", 76, 58, 82, 30),  # overall = 61.5
    ]

    team_a, team_b = balance_teams(players)
    assert abs(team_a.total_strength - team_b.total_strength) == 9.75
    assert len(team_a) == 2 == len(team_b)


def test_odd_team_members():
    players = [
        Player("John Doe", 76, 58, 82, 30),  # overall = 61.5
        Player("Jane Doe", 76, 63, 82, 30),  # overall = 62.75
        Player("J. Doe", 76, 58, 74, 82),  # overall = 72.5
    ]

    team_a, team_b = balance_teams(players)
    assert abs(team_a.total_strength - team_b.total_strength) == 51.75
    assert {len(team_a), len(team_b)} == {1, 2}


def test_non_default_team_names():
    players = [
        Player("John Doe", 76, 58, 82, 30),  # overall = 61.5
        Player("Jane Doe", 76, 63, 82, 30),  # overall = 62.75
    ]

    team_a, team_b = balance_teams(players, "Team Alpha", "Team Bravo")
    assert abs(team_a.total_strength - team_b.total_strength) == 1.25
    assert len(team_a) == 1 == len(team_b)
    assert team_a.name == "Team Alpha"
    assert team_b.name == "Team Bravo"