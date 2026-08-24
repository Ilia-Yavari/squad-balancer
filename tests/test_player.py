from dataclasses import FrozenInstanceError, dataclass

import pytest

from squad_balancer.player import Player


def test_player_creation_and_overall():
    player = Player("John Doe", 76, 58, 82, 30)
    assert player.name == "John Doe"
    assert player.attack == 76
    assert player.defense == 58
    assert player.goalkeeping == 82
    assert player.stamina == 30
    assert player.overall == 61.5

@pytest.mark.parametrize(
    "non_string_name",
    [
        None,
        123,
        False,
    ]
)
def test_non_string_name(non_string_name):
    with pytest.raises(TypeError, match="Player name must be a string, got"):
        Player(non_string_name, 76, 58, 82, 30)


@pytest.mark.parametrize(
    "empty_name",
    [
        (""),
        ("     "),
        ("\t"),
    ]
)
def test_empty_name(empty_name):
    with pytest.raises(ValueError, match="Player name must be non-empty"):
        Player(empty_name, 76, 58, 82, 30)


@pytest.mark.parametrize(
    "name, attack, defense, goalkeeping, stamina",
    [
        ("John Doe", "76", 58, 82, 30),
        ("Jane Doe", 76, True, 82, 30),
        ("J. Doe", 76, 58, False, 82),
        ("JD", 76, 58, 82, "thirty"),
    ],
)
def test_non_integer_stats(
    name,
    attack,
    defense,
    goalkeeping,
    stamina,
):
    with pytest.raises(TypeError, match="must be an integer, got"):
        Player(name, attack, defense, goalkeeping, stamina)


@pytest.mark.parametrize(
    "name, attack, defense, goalkeeping, stamina",
    [
        ("Out of Range High", 101, 50, 50, 50),
        ("Out of Range Low", 50, 0, 50, 50),
    ]
)
def test_out_of_range_stats(
    name,
    attack,
    defense,
    goalkeeping,
    stamina,
):
    with pytest.raises(ValueError, match="must be between 1 and 100, got"):
        Player(name, attack, defense, goalkeeping, stamina)


def test_boundary_stats():
    low_bound_player = Player("John Doe", 1, 1, 1, 1)
    high_bound_player = Player("Jane Doe", 100, 100, 100, 100)

    assert low_bound_player.overall == 1
    assert high_bound_player.overall == 100


@dataclass(frozen=True)
class ExtendedPlayer(Player):
    pace: int = 50


def test_overall_includes_inherited_stats():
    player = ExtendedPlayer("X", 80, 80, 80, 80, pace=10)
    assert player.overall == 66


def test_player_is_immutable():
    player = Player("John Doe", 76, 58, 82, 30)
    with pytest.raises(FrozenInstanceError):
        player.attack = 99


def test_equal_players_are_interchangeable_in_hash_collections():
    twin_a = Player("John Doe", 50, 50, 50, 50)
    twin_b = Player("John Doe", 50, 50, 50, 50)
    assert len({twin_a, twin_b}) == 1

