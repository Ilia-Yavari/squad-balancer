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


@pytest.mark.parametrize("non_string_name", [None, 123, True])
def test_non_string_name(non_string_name, sample_players):
    with pytest.raises(TypeError, match="Team name must be a string"):
        Team(non_string_name, sample_players)


@pytest.mark.parametrize("empty_name", ["", "     ", "\t"])
def test_empty_name(empty_name, sample_players):
    with pytest.raises(ValueError, match="Team name must be non-empty"):
        Team(empty_name, sample_players)


def test_non_tuple_players_type():
    with pytest.raises(TypeError, match="Players must be provided as a tuple"):
        Team("A",
                    [
                        Player("John Doe", 76, 58, 82, 30),
                        Player("Jane Doe", 76, 63, 82, 30),
                        Player("J. Doe", 76, 58, 74, 82),
                        Player("JD", 76, 58, 82, 30)
                    ])


def test_non_player_elements():
    with pytest.raises(TypeError, match="Players must contain only Player instances, got"):
        Team("A", (1, 2))


def test_empty_team():
    team = Team("Empty Team", ())
    assert team.name == "Empty Team"
    assert team.total_strength == 0.0
    assert len(team) == 0


def test_team_is_immutable(sample_players):
    team = Team("Team Alpha", sample_players)
    with pytest.raises(FrozenInstanceError):
        team.name = "New Name"
