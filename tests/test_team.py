from dataclasses import FrozenInstanceError

import pytest

from squad_balancer.player import Player
from squad_balancer.team import Team


@pytest.fixture
def sample_players() -> tuple[Player, ...]:
    return (
        Player("John Doe", 76, 58, 82, 30),
        Player("Jane Doe", 76, 63, 82, 30),
        Player("J. Doe", 76, 58, 74, 82),
        Player("JD", 76, 58, 82, 30),
    )


def test_correct_team_creation(sample_players):
    team = Team("Team Alpha", sample_players)
    assert team.name == "Team Alpha"
    assert team.total_strength == 258.25
    assert len(team) == 4


@pytest.mark.parametrize("invalid_name", [(""), ("   "), None, 123])
def test_invalid_name(invalid_name, sample_players):
    with pytest.raises(ValueError, match="Team name must be a non-empty string."):
        team = Team(invalid_name, sample_players)


def test_invalid_players_type():
    with pytest.raises(TypeError, match="Players must be provided as a tuple."):
        team = Team("A",
                    [
                        Player("John Doe", 76, 58, 82, 30),
                        Player("Jane Doe", 76, 63, 82, 30),
                        Player("J. Doe", 76, 58, 74, 82),
                        Player("JD", 76, 58, 82, 30)
                    ])


def test_empty_team():
    team = Team("Empty Team", ())
    assert team.name == "Empty Team"
    assert team.total_strength == 0.0
    assert len(team) == 0


def test_team_is_immutable(sample_players):
    team = Team("Team Alpha", sample_players)
    with pytest.raises(FrozenInstanceError):
        team.name = "New Name"
