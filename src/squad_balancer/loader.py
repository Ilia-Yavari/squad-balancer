import json
from dataclasses import fields
from pathlib import Path

from squad_balancer.player import Player

_EXPECTED_KEYS = {f.name for f in fields(Player)}


def load_players(path: str | Path) -> list[Player]:
    """Load players from a JSON file containing a list of player records."""
    path = Path(path)

    with open(path, encoding="utf-8") as f:
        records = json.load(f)

    if not isinstance(records, list):
        raise ValueError(f"{path} must contain a list of players, got {type(records).__name__}")

    return [Player(**validate_record(record, index, path)) for index, record in enumerate(records)]


def validate_record(record: object, index: int, path: Path) -> dict:
    """Return record if it is a mapping with exactly the expected player keys, else raise."""
    if not isinstance(record, dict):
        raise TypeError(f"player record {index} in {path} must be an object, got {type(record).__name__}")

    missing = _EXPECTED_KEYS - record.keys()
    unknown = record.keys() - _EXPECTED_KEYS
    if missing or unknown:
        raise TypeError(f"player record {index} in {path} has missing keys {sorted(missing)} or unknown keys {sorted(unknown)}")

    return record
