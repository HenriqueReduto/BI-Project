"""Extract data/raw/*.csv.gz without changing originals or existing CSVs.

Run from any directory: python "path/to/BI Project/scripts/extract_csv_gz.py"
Uses only Python's standard library. Output: name.csv.gz -> name.extracted.csv.
"""

import argparse
import gzip
from pathlib import Path
import shutil
import sys


def extract(source: Path, destination: Path) -> bool:
    """Stream the full gzip payload; remove our partial output on failure."""
    try:
        output = destination.open("xb")
    except FileExistsError:
        print(f"SKIP (already exists): {destination.name}", flush=True)
        return False
    try:
        with output, gzip.open(source, "rb") as compressed:
            shutil.copyfileobj(compressed, output, length=1024 * 1024)
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
    print(f"EXTRACTED: {source.name} -> {destination.name} "
          f"({destination.stat().st_size:,} bytes)", flush=True)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw-dir", type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "raw",
        help="Folder containing .csv.gz files (default: project data/raw).",
    )
    args = parser.parse_args()
    if not args.raw_dir.is_dir():
        parser.error(f"Raw data folder does not exist: {args.raw_dir}")
    sources = sorted(args.raw_dir.glob("*.csv.gz"))
    if not sources:
        print(f"No .csv.gz files found in {args.raw_dir}")
        return 0
    failed = 0
    for source in sources:
        destination = source.with_name(source.name[:-7] + ".extracted.csv")
        try:
            extract(source, destination)
        except (OSError, EOFError) as error:
            print(f"ERROR: {source.name}: {error}", file=sys.stderr, flush=True)
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
