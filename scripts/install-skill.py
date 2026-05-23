from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_TARGETS = {
    "codex": Path.home() / ".codex" / "skills" / "the-polyglot-protocol",
    "claude-code": Path.home() / ".claude" / "skills" / "the-polyglot-protocol",
    "opencode": Path.home() / ".opencode" / "skills" / "the-polyglot-protocol",
}

EXCLUDES = {".git", ".venv", "__pycache__"}


def copy_project(target: Path, *, force: bool) -> None:
    if target.exists():
        if not force:
            raise SystemExit(
                f"target already exists: {target}\n"
                "rerun with --force to replace it"
            )
        shutil.rmtree(target)

    def ignore(_: str, names: list[str]) -> set[str]:
        return {name for name in names if name in EXCLUDES}

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT, target, ignore=ignore)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install The Polyglot Protocol skill.")
    parser.add_argument(
        "--agent",
        choices=sorted(DEFAULT_TARGETS),
        default="codex",
        help="coding agent skill location to install into",
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="custom target directory; overrides --agent default",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing installed copy",
    )
    args = parser.parse_args()

    target = args.target.expanduser() if args.target else DEFAULT_TARGETS[args.agent]
    copy_project(target, force=args.force)
    print(f"installed The Polyglot Protocol for {args.agent}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
