from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Mirror a markdown best-practices folder into a target output folder "
            "for later language/framework-specific rewriting."
        )
    )
    parser.add_argument("--source", required=True, help="Source guide folder")
    parser.add_argument("--output", required=True, help="Output guide folder")
    parser.add_argument("--language", required=True, help="Target language")
    parser.add_argument("--framework", default="", help="Target framework")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing markdown files in the output folder",
    )
    return parser.parse_args()


def build_header(source_file: Path, language: str, framework: str) -> str:
    framework_value = framework or "none"
    return (
        "<!--\n"
        f"Source: {source_file.resolve()}\n"
        f"Target language: {language}\n"
        f"Target framework: {framework_value}\n"
        "Status: Rewrite this file with stack-specific guidance before final delivery.\n"
        "-->\n\n"
    )


def main() -> int:
    args = parse_args()
    source = Path(args.source).resolve()
    output = Path(args.output).resolve()

    if not source.is_dir():
        raise SystemExit(f"Source folder does not exist or is not a directory: {source}")

    output.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0

    for source_file in sorted(source.rglob("*.md")):
        relative_path = source_file.relative_to(source)
        target_file = output / relative_path
        target_file.parent.mkdir(parents=True, exist_ok=True)

        if target_file.exists() and not args.overwrite:
            skipped += 1
            continue

        source_text = source_file.read_text(encoding="utf-8")
        scaffold_text = build_header(source_file, args.language, args.framework) + source_text
        target_file.write_text(scaffold_text, encoding="utf-8")
        created += 1

    print(f"Scaffolded {created} markdown file(s) into {output}")
    if skipped:
        print(f"Skipped {skipped} existing markdown file(s)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
