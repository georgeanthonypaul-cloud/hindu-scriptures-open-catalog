#!/usr/bin/env python3
"""Download only rights-approved resources from the mirror manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "catalog" / "mirror_manifest.csv"
USER_AGENT = "hindu-scriptures-open-catalog/0.1 (+rights-first research mirror)"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    approved = [row for row in rows if row["status"] == "approved"]
    for row in approved:
        destination = (ROOT / row["destination"]).resolve()
        if ROOT.resolve() not in destination.parents:
            raise SystemExit(f"Unsafe destination outside repository: {destination}")
        if args.dry_run:
            print(f"WOULD FETCH {row['id']} -> {destination.relative_to(ROOT)}")
            continue
        if destination.exists() and not args.force:
            payload = destination.read_bytes()
            print(f"EXISTS {row['id']} sha256={digest(payload)}")
        else:
            payload = fetch(row["source_url"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
            print(f"FETCHED {row['id']} bytes={len(payload)} sha256={digest(payload)}")
        actual_sha = digest(payload)
        expected_sha = row["sha256"].strip()
        if expected_sha and expected_sha != actual_sha:
            raise SystemExit(f"Checksum mismatch for {row['id']}: expected {expected_sha}, got {actual_sha}")
        metadata = {
            "id": row["id"],
            "title": row["title"],
            "layer": row["layer"],
            "source_id": row["source_id"],
            "source_url": row["source_url"],
            "license_id": row["license_id"],
            "license_url": row["license_url"],
            "attribution": row["attribution"],
            "verified_on": row["verified_on"],
            "verification_note": row["verification_note"],
            "sha256": actual_sha,
        }
        metadata_path = destination.with_suffix(destination.suffix + ".metadata.json")
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

