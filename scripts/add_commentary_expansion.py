#!/usr/bin/env python3
"""Append major Vedic, epic, Purāṇic, and Dharmaśāstra commentary routes."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "catalog" / "commentaries.csv"

FIELDS = [
    "school", "commentator_or_author", "work_or_commentary", "relationship_type", "base_text",
    "resource", "host", "url", "access", "rights", "mirror_status", "notes",
]

ROWS = [
    ("Vedic exegesis", "Sāyaṇa", "Ṛgvedabhāṣya", "Vedic bhāṣya", "Rigveda Samhita", "Internet Archive edition discovery", "Internet Archive", "https://archive.org/search?query=Sayana+Rigveda+Bhashya", "Free access", "Item-by-item; verify edition and scan rights", "link-only-pending-rights", "Record recension and edition; do not attach one Vedic commentary to unrelated recensions."),
    ("Vedic exegesis", "Sāyaṇa", "Sāmavedabhāṣya", "Vedic bhāṣya", "Samaveda Samhita", "Internet Archive edition discovery", "Internet Archive", "https://archive.org/search?query=Sayana+Samaveda+Bhashya", "Free access", "Item-by-item; verify edition and scan rights", "link-only-pending-rights", "Historical Sanskrit editions may be public domain; modern translations may not be."),
    ("Vedic exegesis", "Sāyaṇa", "Taittirīyasaṃhitābhāṣya and related Yajurvedic bhāṣyas", "Vedic bhāṣya", "Yajurveda Samhita", "Internet Archive edition discovery", "Internet Archive", "https://archive.org/search?query=Sayana+Yajurveda+Bhashya", "Free access", "Item-by-item; verify edition and scan rights", "link-only-pending-rights", "Identify Śukla/Kṛṣṇa Yajurveda recension before linking a commentary."),
    ("Vedic exegesis", "Sāyaṇa", "Atharvavedabhāṣya (traditional attribution/editorial history requires review)", "Vedic bhāṣya", "Atharvaveda Samhita", "Internet Archive edition discovery", "Internet Archive", "https://archive.org/search?query=Atharvaveda+Sayana+Bhashya", "Free access", "Item-by-item; verify edition and attribution", "link-only-pending-rights", "Do not present the commentary's authorship history as uncontested."),
    ("Advaita Vedānta", "Ādi Śaṅkara", "Principal Upaniṣad Bhāṣyas", "Upaniṣad commentaries", "Principal Upanishads", "Gita Supersite Upaniṣad portal", "IIT Kanpur", "https://www.gitasupersite.iitk.ac.in/", "Free to read", "Sanskrit base/commentaries and modern translations have different rights", "link-only-pending-rights", "Map each bhāṣya to its exact Upaniṣad and edition rather than treating all 108 as Śaṅkara-commented."),
    ("Viśiṣṭādvaita", "Raṅgarāmānuja Muni", "Upaniṣad Bhāṣyas", "Upaniṣad commentaries", "Principal Upanishads", "Internet Archive discovery", "Internet Archive", "https://archive.org/search?query=Rangaramanaja+Upanishad+Bhashya", "Free access", "Item-by-item; verify spelling, edition, and scan rights", "link-only-pending-rights", "Important Śrī Vaiṣṇava route; title and transliteration variants require authority control."),
    ("Dvaita Vedānta", "Madhvācārya", "Upaniṣad Bhāṣyas", "Upaniṣad commentaries", "Principal Upanishads", "Internet Archive discovery", "Internet Archive", "https://archive.org/search?query=Madhva+Upanishad+Bhashya", "Free access", "Item-by-item; verify edition and translation rights", "link-only-pending-rights", "Record each Upaniṣad separately and distinguish Madhva's bhāṣya from later ṭīkās."),
    ("Bhāgavata tradition", "Śrīdhara Svāmin", "Bhāvārthadīpikā", "Purāṇa commentary", "Bhagavata Purana", "Internet Archive discovery", "Internet Archive", "https://archive.org/search?query=Sridhara+Svamin+Bhavarthadipika", "Free access", "Item-by-item; modern editions/translations may be protected", "link-only-pending-rights", "Influential cross-tradition commentary on the Bhāgavata Purāṇa."),
    ("Mahābhārata exegesis", "Nīlakaṇṭha Caturdhara", "Bhāratabhāvadīpa / Nīlakaṇṭhī", "Epic commentary", "Mahabharata", "Internet Archive discovery", "Internet Archive", "https://archive.org/search?query=Nilakantha+Mahabharata+commentary", "Free access", "Item-by-item; verify historical edition", "link-only-pending-rights", "Map commentary coverage by parvan and identify the printed edition."),
    ("Rāmāyaṇa exegesis", "Govindarāja", "Bhūṣaṇa", "Epic commentary", "Ramayana", "Internet Archive discovery", "Internet Archive", "https://archive.org/search?query=Govindaraja+Ramayana+Bhushana", "Free access", "Item-by-item; verify edition", "link-only-pending-rights", "One major Rāmāyaṇa commentary tradition; Uttarakāṇḍa treatment varies by edition."),
    ("Rāmāyaṇa exegesis", "Maheśvaratīrtha", "Tattvadīpa", "Epic commentary", "Ramayana", "Internet Archive discovery", "Internet Archive", "https://archive.org/search?query=Mahesvaratirtha+Tattvadipa+Ramayana", "Free access", "Item-by-item; verify edition", "link-only-pending-rights", "Record the exact edition and kāṇḍa coverage."),
    ("Dharmaśāstra", "Medhātithi", "Manubhāṣya", "Smṛti commentary", "Manu Smriti", "SARIT and Internet Archive discovery", "GitHub / Internet Archive", "https://github.com/sarit/SARIT-corpus/search?q=Medhatithi&type=code", "Discovery", "File- or item-specific", "link-only-pending-rights", "Separate the Manu root text from Medhātithi's commentary and later editorial apparatus."),
    ("Dharmaśāstra", "Kullūka Bhaṭṭa", "Manvarthamuktāvalī", "Smṛti commentary", "Manu Smriti", "Internet Archive discovery", "Internet Archive", "https://archive.org/search?query=Kulluka+Manvarthamuktavali", "Free access", "Item-by-item; verify edition", "link-only-pending-rights", "Later influential commentary; compare with Medhātithi rather than silently harmonizing them."),
    ("Dharmaśāstra", "Vijñāneśvara", "Mitākṣarā", "Smṛti commentary", "Yajnavalkya Smriti", "SARIT direct route", "GitHub", "https://github.com/sarit/SARIT-corpus/blob/master/vijnanesvara-mitaksara.xml", "Open-license candidate", "Inspect TEI availability statement before mirroring", "link-only-pending-rights", "Important jurisprudential commentary; edition-level license still needs manifest review."),
]


def main() -> None:
    with TARGET.open(encoding="utf-8", newline="") as handle:
        existing = list(csv.DictReader(handle))
    keys = {(row["commentator_or_author"], row["work_or_commentary"], row["base_text"]) for row in existing}
    additions = [dict(zip(FIELDS, values)) for values in ROWS if (values[1], values[2], values[4]) not in keys]
    with TARGET.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(existing + additions)
    print(f"Added {len(additions)} commentary mappings; total {len(existing) + len(additions)}")


if __name__ == "__main__":
    main()

