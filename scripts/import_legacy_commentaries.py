#!/usr/bin/env python3
"""One-time importer for the earlier researched scholar directory."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Path to hindu_resources_data.json")
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8"))
    rows = []
    for item in data["scholars"]:
        rows.append(
            {
                "school": item["school"],
                "commentator_or_author": item["scholar"],
                "work_or_commentary": item["work"],
                "relationship_type": item["kind"],
                "base_text": "",
                "resource": item["resource"],
                "host": item["host"],
                "url": item["url"],
                "access": item["access"],
                "rights": item["rights"],
                "mirror_status": "approved" if item["access"].startswith("CC ") else "link-only-pending-rights",
                "notes": item["notes"],
            }
        )
    target = ROOT / "catalog" / "commentaries.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} commentary/scholar records to {target}")


if __name__ == "__main__":
    main()

