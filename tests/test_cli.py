import json

import pytest

from squad_balancer.cli import main


@pytest.fixture
def squad_file(tmp_path):
    records = [
        {"name": "John Doe", "attack": 76, "defense": 58, "goalkeeping": 82, "stamina": 30},
        {"name": "Jane Doe", "attack": 76, "defense": 63, "goalkeeping": 82, "stamina": 30},
        {"name": "J. Doe", "attack": 76, "defense": 58, "goalkeeping": 74, "stamina": 82},
        {"name": "JD", "attack": 76, "defense": 58, "goalkeeping": 82, "stamina": 30},
    ]
    file = tmp_path / "squad.json"
    file.write_text(json.dumps(records), encoding="utf-8")
    return file


def test_balances_file_and_prints_teams(squad_file, capsys):
    exit_code = main([str(squad_file)])

    out = capsys.readouterr().out
    assert exit_code == 0
    assert "Team A" in out
    assert "Team B" in out
    assert "John Doe" in out
    assert "Strength difference: 9.75" in out


def test_custom_team_names_appear_in_output(squad_file, capsys):
    exit_code = main([str(squad_file), "-a", "Reds", "-b", "Blues"])

    out = capsys.readouterr().out
    assert exit_code == 0
    assert "Reds" in out
    assert "Blues" in out


def test_missing_file_reports_error_on_stderr(tmp_path, capsys):
    exit_code = main([str(tmp_path / "nope.json")])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error:" in captured.err
    assert captured.out == ""


def test_invalid_domain_value_reports_error_on_stderr(tmp_path, capsys):
    file = tmp_path / "bad.json"
    file.write_text(
        json.dumps([{"name": "X", "attack": 999, "defense": 50, "goalkeeping": 50, "stamina": 50}]),
        encoding="utf-8",
    )

    exit_code = main([str(file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "attack must be between 1 and 100" in captured.err


def test_document_not_a_list_reports_error_on_stderr(tmp_path, capsys):
    file = tmp_path / "shaped.json"
    file.write_text(json.dumps({"players": []}), encoding="utf-8")

    exit_code = main([str(file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "must contain a list of players" in captured.err
