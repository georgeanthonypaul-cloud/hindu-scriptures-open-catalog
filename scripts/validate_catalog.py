#!/usr/bin/env python3
"""Validate required fields, uniqueness, URLs, rights states, and mirrored checksums."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"


def load_csv(name: str) -> list[dict[str, str]]:
    with (CATALOG / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def main() -> None:
    errors: list[str] = []
    texts = load_csv("texts.csv")
    commentaries = load_csv("commentaries.csv")
    sources = load_csv("sources.csv")
    manifest = load_csv("mirror_manifest.csv")
    source_ids = {row["source_id"] for row in sources}

    text_ids = [row["id"] for row in texts]
    duplicates = [key for key, count in Counter(text_ids).items() if count > 1]
    if duplicates:
        errors.append(f"Duplicate text IDs: {duplicates}")
    for row in texts:
        for key in ["id", "category", "subgroup", "title", "catalog_status", "mirror_status"]:
            if not row.get(key, "").strip():
                errors.append(f"texts.csv {row.get('id') or '<missing-id>'}: missing {key}")
        if row.get("candidate_source") and not valid_url(row["candidate_source"]):
            errors.append(f"texts.csv {row['id']}: invalid candidate_source")

    for index, row in enumerate(commentaries, start=2):
        if not row.get("commentator_or_author", "").strip() or not row.get("work_or_commentary", "").strip():
            errors.append(f"commentaries.csv row {index}: missing author or work")
        if row.get("url") and not valid_url(row["url"]):
            errors.append(f"commentaries.csv row {index}: invalid URL")

    allowed = {"approved", "pending", "link-only", "blocked"}
    destinations: set[str] = set()
    for row in manifest:
        if row["status"] not in allowed:
            errors.append(f"manifest {row['id']}: invalid status {row['status']}")
        if row["source_id"] not in source_ids:
            errors.append(f"manifest {row['id']}: unknown source_id {row['source_id']}")
        if not valid_url(row["source_url"]):
            errors.append(f"manifest {row['id']}: invalid source URL")
        if row["status"] == "approved" and not all(row.get(key, "").strip() for key in ["license_id", "license_url", "attribution", "verified_on", "verification_note", "sha256"]):
            errors.append(f"manifest {row['id']}: approved row lacks rights evidence")
        if row["destination"] in destinations:
            errors.append(f"manifest {row['id']}: duplicate destination")
        destinations.add(row["destination"])
        path = ROOT / row["destination"]
        if row["status"] == "approved" and not path.exists():
            errors.append(f"manifest {row['id']}: approved payload is missing")
        if path.exists():
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            expected = row["sha256"].strip()
            if expected and expected != actual:
                errors.append(f"manifest {row['id']}: checksum mismatch")
            metadata = path.with_suffix(path.suffix + ".metadata.json")
            if not metadata.exists():
                errors.append(f"manifest {row['id']}: missing metadata sidecar")
            else:
                try:
                    data = json.loads(metadata.read_text(encoding="utf-8"))
                    if data.get("sha256") != actual:
                        errors.append(f"manifest {row['id']}: sidecar checksum mismatch")
                except (ValueError, OSError) as exc:
                    errors.append(f"manifest {row['id']}: invalid sidecar: {exc}")

    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"VALID: {len(texts)} text records, {len(commentaries)} commentary/scholar records, {len(sources)} sources, {len(manifest)} mirror entries")


if __name__ == "__main__":
    main()
