#!/usr/bin/env python3
"""Populate mirror-manifest SHA-256 fields from downloaded files."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "catalog" / "mirror_manifest.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise SystemExit("Mirror manifest has no header")

    updated = 0
    for row in rows:
        path = ROOT / row["destination"]
        if path.exists():
            actual = sha256(path)
            if row.get("sha256") != actual:
                row["sha256"] = actual
                updated += 1

    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"UPDATED: {updated} checksum fields")


if __name__ == "__main__":
    main()
