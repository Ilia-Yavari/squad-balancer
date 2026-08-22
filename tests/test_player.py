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
    "invalid_name",
    [
        (""),
        ("   "),
        None,
        123,
    ]
)
def test_invalid_name(invalid_name):
    with pytest.raises(ValueError, match="Player name must be a non-empty string."):
        player = Player(invalid_name, 76, 58, 82, 30)


@pytest.mark.parametrize(
    "name, attack, defense, goalkeeping, stamina",
    [
        ("John Doe", "76", 58, 82, 30),
        ("Jane Doe", 76, True, 82, 30),
        ("J. Doe", 76, 58, False, 82),
        ("JD", 76, 58, 82, "thirty"),
        ("Out of Range High", 101, 50, 50, 50),
        ("Out of Range Low", 50, 0, 50, 50),
    ],
)
def test_invalid_stats(
        name,
        attack,
        defense,
        goalkeeping,
        stamina,
):
    with pytest.raises(ValueError, match="must be an integer between 1 and 100, got"):
        Player(name, attack, defense, goalkeeping, stamina)

