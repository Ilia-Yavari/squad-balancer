import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from squad_balancer.balancer import balance_teams
from squad_balancer.loader import load_players
from squad_balancer.team import Team


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="squad-balancer",
        description="Split a group of football players into two balanced teams.",
    )
    parser.add_argument("path", type=Path, help="path to a JSON file containing player records")
    parser.add_argument("-a", "--team-a", default="Team A", help="name of the first team (default: %(default)s)")
    parser.add_argument("-b", "--team-b", default="Team B", help="name of the second team (default: %(default)s)")
    return parser


def format_team(team: Team) -> str:
    width = max((len(player.name) for player in team.players), default=0)
    lines = [f"{team.name}  (total strength {team.total_strength:.2f})"]
    for player in sorted(team.players, key=lambda p: p.overall, reverse=True):
        lines.append(f"  {player.name:<{width}}  overall {player.overall:.2f}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        players = load_players(args.path)
        team_a, team_b = balance_teams(players, args.team_a, args.team_b)
    except (OSError, ValueError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(format_team(team_a))
    print(format_team(team_b))
    print(f"\nStrength difference: {abs(team_a.total_strength - team_b.total_strength):.2f}")
    return 0
