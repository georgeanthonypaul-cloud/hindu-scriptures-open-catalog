#!/usr/bin/env python3
"""Apply edition-level mirror coverage states to the requested-text catalogue."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "texts.csv"
STATS = ROOT / "catalog" / "stats.json"

ENGLISH = {
    "upanisad-aitareya",
    "upanisad-kaushitaki",
    "upanisad-isha",
    "upanisad-brihadaranyaka",
    "upanisad-katha",
    "upanisad-taittiriya",
    "upanisad-shvetashvatara",
    "upanisad-maitrayani",
    "upanisad-chandogya",
    "upanisad-kena",
    "upanisad-mundaka",
    "upanisad-prashna",
    "itihasa-harivamsa",
    "purana-vishnu-purana",
}

SANSKRIT = {
    "itihasa-ramayana",
    "itihasa-bala-kanda",
    "itihasa-ayodhya-kanda",
    "itihasa-aranya-kanda",
    "itihasa-kishkindha-kanda",
    "itihasa-sundara-kanda",
    "itihasa-yuddha-kanda",
    "itihasa-uttara-kanda",
    "purana-brahma-purana",
    "dharmasastra-manu-smriti",
    "dharmasastra-narada-smriti",
    "dharmasastra-yajnavalkya-smriti",
    "upaveda-sastra-charaka-samhita",
    "upaveda-sastra-sushruta-samhita",
    "upaveda-sastra-chanakya-arthashastra",
    "darsana-nyaya-sutras",
}

SANSKRIT_AND_ENGLISH = {
    "itihasa-mahabharata",
    "itihasa-adi-parva",
    "itihasa-sabha-parva",
    "itihasa-vana-parva",
    "itihasa-virata-parva",
    "itihasa-udyoga-parva",
    "itihasa-bhishma-parva",
    "itihasa-bhagavad-gita",
    "itihasa-drona-parva",
    "itihasa-karna-parva",
    "itihasa-shalya-parva",
    "itihasa-sauptika-parva",
    "itihasa-stri-parva",
    "itihasa-shanti-parva",
    "itihasa-anushasana-parva",
    "itihasa-ashvamedhika-parva",
    "itihasa-ashramavasika-parva",
    "itihasa-mausala-parva",
    "itihasa-mahaprasthanika-parva",
    "itihasa-svargarohana-parva",
    "darsana-yoga-sutras",
}

ENGLISH_COMMENTARIES = {"darsana-brahma-sutras"}
PARTIAL_SANSKRIT = {"purana-skanda-purana"}


def main() -> None:
    with CATALOG.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise SystemExit("texts.csv has no header")

    updated = 0
    for row in rows:
        text_id = row["id"]
        status = None
        if text_id in SANSKRIT_AND_ENGLISH:
            status = "mirrored-sanskrit-and-public-domain-english"
        elif text_id in ENGLISH:
            status = "mirrored-public-domain-english"
        elif text_id in SANSKRIT:
            status = "mirrored-open-license-sanskrit"
        elif text_id in ENGLISH_COMMENTARIES:
            status = "mirrored-public-domain-english-commentaries"
            row["commentary_status"] = "commentary-mirrored"
        elif text_id in PARTIAL_SANSKRIT:
            status = "partial-open-license-sanskrit"
        if status and row["mirror_status"] != status:
            row["mirror_status"] = status
            updated += 1
        if text_id in {"darsana-nyaya-sutras", "darsana-yoga-sutras"}:
            row["commentary_status"] = "commentary-mirrored"

    with CATALOG.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    stats = {
        "total_text_records": len(rows),
        "by_category": dict(sorted(Counter(row["category"] for row in rows).items())),
        "by_mirror_status": dict(
            sorted(Counter(row["mirror_status"] for row in rows).items())
        ),
        "generated_from": "scripts/update_coverage_status.py",
        "scope_note": (
            "Coverage is edition-specific. A mirrored translation or partial edition does not "
            "establish complete Sanskrit-and-English coverage of a title."
        ),
    }
    STATS.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"UPDATED: {updated} catalogue coverage states")


if __name__ == "__main__":
    main()
