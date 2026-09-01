import json
from pathlib import Path

import pytest

from squad_balancer.loader import load_players
from squad_balancer.player import Player


def write_file(tmp_path: Path, text: str) -> Path:
    file = tmp_path / "players.json"
    file.write_text(text, encoding="utf-8")
    return file


VALID_RECORDS = json.dumps([
    {"name": "John Doe", "attack": 76, "defense": 58, "goalkeeping": 82, "stamina": 30},
    {"name": "Jane Doe", "attack": 76, "defense": 63, "goalkeeping": 82, "stamina": 30},
])


@pytest.mark.parametrize("as_string", [False, True], ids=["path", "str"])
def test_loads_players_from_valid_file(tmp_path, as_string):
    file = write_file(tmp_path, VALID_RECORDS)

    players = load_players(str(file) if as_string else file)

    assert players == [
        Player("John Doe", 76, 58, 82, 30),
        Player("Jane Doe", 76, 63, 82, 30),
    ]


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_players(tmp_path / "does_not_exist.json")


def test_invalid_json_syntax_raises_decode_error(tmp_path):
    file = write_file(tmp_path, '[{"name": "John", attack: 76}]')

    with pytest.raises(json.JSONDecodeError):
        load_players(file)


@pytest.mark.parametrize(
    "document, actual_type",
    [
        ({"players": []}, "dict"),
        (42, "int"),
    ],
)
def test_document_not_a_list_raises_value_error(tmp_path, document, actual_type):
    file = write_file(tmp_path, json.dumps(document))

    with pytest.raises(ValueError, match=f"must contain a list of players, got {actual_type}"):
        load_players(file)


@pytest.mark.parametrize(
    "bad_record, match",
    [
        (
            {"name": "John Doe", "attack": 76, "defense": 58, "goalkeping": 82, "stamina": 30},
            r"missing keys \['goalkeeping'\]",
        ),
        (
            {"name": "John Doe", "attack": 76, "defense": 58, "goalkeeping": 82, "stamina": 30, "pace": 90},
            r"unknown keys \['pace'\]",
        ),
    ],
)
def test_record_with_wrong_keys_raises_type_error(tmp_path, bad_record, match):
    good_record = {"name": "Jane Doe", "attack": 76, "defense": 63, "goalkeeping": 82, "stamina": 30}
    file = write_file(tmp_path, json.dumps([good_record, bad_record]))

    with pytest.raises(TypeError, match=match):
        load_players(file)


@pytest.mark.parametrize(
    "bad_record, actual_type",
    [
        (["John Doe", 76, 58, 82, 30], "list"),
        ("John Doe", "str"),
    ],
)
def test_record_not_an_object_raises_type_error(tmp_path, bad_record, actual_type):
    file = write_file(tmp_path, json.dumps([bad_record]))

    with pytest.raises(TypeError, match=f"player record 0 .* must be an object, got {actual_type}"):
        load_players(file)


def test_invalid_domain_value_propagates_from_player(tmp_path):
    file = write_file(
        tmp_path,
        json.dumps([{"name": "John Doe", "attack": 999, "defense": 58, "goalkeeping": 82, "stamina": 30}]),
    )

    with pytest.raises(ValueError, match="attack must be between 1 and 100, got 999"):
        load_players(file)
