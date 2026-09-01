# Squad Balancer

[![CI](https://github.com/Ilia-Yavari/squad-balancer/actions/workflows/ci.yml/badge.svg)](https://github.com/Ilia-Yavari/squad-balancer/actions/workflows/ci.yml)

Split a group of football players into two balanced teams.

Given a JSON file describing players with attack, defense, goalkeeping and
stamina ratings (each 1–100), Squad Balancer finds the split whose total
strength difference is minimal. The search is exhaustive over all possible
partitions — exact, not heuristic, which is entirely feasible for
squad-sized groups.

## Features

- **Validated domain model** — every player is checked at construction
  (name, stat types, stat ranges); invalid data can never enter a team.
- **Exact balancing** — the best partition by total strength, not a
  greedy approximation.
- **JSON input** — structural validation with precise error messages
  (file, record index, missing and unknown keys).
- **Immutable values** — players and teams are frozen dataclasses; a
  loaded squad cannot be mutated by accident.

## Installation

Requires Python 3.10+.

```bash
pip install -e .
```

## Usage

Balance the bundled example squad:

```bash
squad-balancer examples/players.json
```

```
Team A  (total strength 186.25)
  Sara Ahmadi  overall 62.50
  Mike Brown   overall 62.50
  Ali Rezaei   overall 61.25
Team B  (total strength 184.50)
  John Smith   overall 65.00
  David Kim    overall 64.50
  Reza Karimi  overall 55.00

Strength difference: 1.75
```

Name the teams anything you like:

```bash
squad-balancer examples/players.json -a "Reds" -b "Blues"
```

The same command works as `python -m squad_balancer examples/players.json`.

## Input format

A JSON array of player objects. All four stats are required and must be
integers from 1 to 100.

```json
[
    {"name": "Ali Rezaei", "attack": 85, "defense": 40, "goalkeeping": 30, "stamina": 90},
    {"name": "John Smith", "attack": 60, "defense": 75, "goalkeeping": 45, "stamina": 80}
]
```

Malformed input is reported precisely — for example:

```
Error: player record 0 in squad.json has missing keys ['goalkeeping'] or unknown keys ['goalkeping']
```

## As a library

```python
from squad_balancer.balancer import balance_teams
from squad_balancer.loader import load_players

players = load_players("examples/players.json")
team_a, team_b = balance_teams(players, "Reds", "Blues")
```

## Project structure

```
src/squad_balancer/
├── player.py     # Player: validated, frozen dataclass with overall rating
├── team.py       # Team: frozen roster with total strength
├── balancer.py   # balance_teams: exhaustive best-partition search
├── loader.py     # load_players: JSON input with structural validation
└── cli.py        # command-line entry point
tests/            # unit tests for every module
examples/         # a ready-to-run example squad
```

## Development

```bash
pip install -e .[dev]
pytest
```

## License

[MIT](LICENSE)
