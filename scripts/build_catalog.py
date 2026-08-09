#!/usr/bin/env python3
"""Build the requested scripture catalogue from a reviewable seed list."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"


def split_items(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


SECTIONS = [
    (
        "Śruti",
        "Vedic Saṃhitā",
        split_items("Rigveda Samhita|Samaveda Samhita|Yajurveda Samhita|Atharvaveda Samhita"),
    ),
    (
        "Śruti",
        "Brāhmaṇa",
        split_items("Aitareya Brahmana|Kaushitaki Brahmana|Shatapatha Brahmana|Taittiriya Brahmana|Gopatha Brahmana"),
    ),
    (
        "Śruti",
        "Āraṇyaka / requested structural layer",
        split_items("Aitareya Aranyaka|Kaushitaki Aranyaka|Brihadaranyaka Aranyaka|Taittiriya Aranyaka|Maitrayani Aranyaka"),
    ),
    (
        "Upaniṣad",
        "Requested 108-title list",
        split_items(
            "Aitareya|Kaushitaki|Mudgala|Atma-Bodha|Nirvana|Akshamalika|Tripura|Saubhagya-Lakshmi|Bahvricha|Nadabindu|"
            "Isha|Brihadaranyaka|Jabala|Hamsa|Paramahamsa|Subala|Mantrika|Niralamba|Trishikhi-Brahmana|Mandala-Brahmana|"
            "Advayataraka|Paingala|Bhikshu|Turiyatita|Adhyatma|Tarasara|Yajnavalkya|Satyayani|Muktika|Katha|Taittiriya|"
            "Shvetashvatara|Maitrayani|Garbha|Brahma|Kaivalya|Kalagni-Rudra|Mahanarayana|Amritabindu|Amritanada|Kshurika|"
            "Tejobindu|Dhyanabindu|Brahmavidya|Yogatattva|Dakshinamurti|Skanda|Shariraka|Yoga-Shikha|Ekakshara|Akshi|"
            "Avadhuta|Katharudra|Rudrahridaya|Panchabrahma|Pranagnihotra|Sarasvati-Rahasya|Sukarahasya|Varaha|Yogakundali|"
            "Kalisantarana|Chandogya|Kena|Aruni|Maitreya|Vajrasuchi|Vasudeva|Avyakta|Kundika|Jabala-Darshana|"
            "Yogachudamani|Samnyasa|Mahat|Savitri|Rudraksha-Jabala|Jabali|Mundaka|Mandukya|Prashna|Surya|Atma|Khechari|"
            "Palani|Shaundilya|Narada-Parivrajaka|Parabrahma|Paramahamsa-Parivrajaka|Pasupata-Brahma|Mahavakya|Krishna|"
            "Garuda|Gopalatapini|Dattatreya|Nrsimhatapini|Ramatapini|Ramarahasya|Hayagriva|Atharvashikha|Atharvashira|"
            "Ganapati|Brihajjabala|Bhasmajabala|Sharabha|Annapurna|Tripuratapini|Devi|Bhavana|Sita"
        ),
    ),
    (
        "Itihāsa",
        "Rāmāyaṇa",
        split_items("Ramayana|Bala Kanda|Ayodhya Kanda|Aranya Kanda|Kishkindha Kanda|Sundara Kanda|Yuddha Kanda|Uttara Kanda"),
    ),
    (
        "Itihāsa",
        "Mahābhārata",
        split_items(
            "Mahabharata|Adi Parva|Sabha Parva|Vana Parva|Virata Parva|Udyoga Parva|Bhishma Parva|Bhagavad Gita|"
            "Drona Parva|Karna Parva|Shalya Parva|Sauptika Parva|Stri Parva|Shanti Parva|Anushasana Parva|"
            "Ashvamedhika Parva|Ashramavasika Parva|Mausala Parva|Mahaprasthanika Parva|Svargarohana Parva|Harivamsa"
        ),
    ),
    (
        "Purāṇa",
        "Mahāpurāṇa and requested Upapurāṇa scope",
        split_items(
            "Brahma Purana|Padma Purana|Vishnu Purana|Shiva Purana|Bhagavata Purana|Naradiya Purana|Markandeya Purana|"
            "Agni Purana|Bhavishya Purana|Brahmavaivarta Purana|Linga Purana|Varaha Purana|Skanda Purana|Vamana Purana|"
            "Kurma Purana|Matsya Purana|Garuda Purana|Brahmanda Purana|Ganesha Purana|Mudgala Purana|Devi-Bhagavata Purana|"
            "Kalika Purana|Kapila Purana|Sanatkumara Purana|Samba Purana|Bhargava Purana"
        ),
    ),
    (
        "Dharmaśāstra",
        "Dharmasūtra",
        split_items("Gautama Dharmasutra|Baodhayana Dharmasutra|Apastamba Dharmasutra|Vasistha Dharmasutra"),
    ),
    (
        "Dharmaśāstra",
        "Smṛti",
        split_items(
            "Manu Smriti|Yajnavalkya Smriti|Parashara Smriti|Narada Smriti|Vishnu Smriti|Atri Smriti|Harita Smriti|"
            "Usanas Smriti|Angiras Smriti|Yama Smriti|Apastamba Smriti|Samvarta Smriti|Katyayana Smriti|Brihaspati Smriti|"
            "Shankha Smriti|Likhita Smriti|Daksha Smriti|Shatatapa Smriti|Vriddha-Gautama Smriti|Vyasa Smriti|Jabali Smriti|"
            "Nachiketa Smriti|Chhandas Smriti|Laugakshi Smriti|Kashyapa Smriti|Sanatkumara Smriti|Shatadru Smriti|"
            "Janaka Smriti|Vyaghra Smriti|Jatukarnya Smriti|Kapinjala Smriti|Vishvamitra Smriti"
        ),
    ),
    (
        "Vedāṅga",
        "Auxiliary Vedic disciplines",
        split_items("Paniniya Shiksha|Pingala Chandasutras|Ashtadhyayi|Yaska Nirukta|Vedanga Jyotisha|Shrautasutras|Grihyasutras|Sulbasutras"),
    ),
    (
        "Upaveda / Śāstra",
        "Medicine, polity, arts, and architecture",
        split_items("Charaka Samhita|Sushruta Samhita|Dhanurveda Sutra|Gandharvaveda Sutra|Chanakya Arthashastra|Manasara Shilpa Shastra"),
    ),
    (
        "Darśana",
        "Foundational sūtras",
        split_items("Nyaya Sutras|Vaisheshika Sutras|Samkhya Sutras|Yoga Sutras|Mimamsa Sutras|Brahma Sutras"),
    ),
    (
        "Āgama / Tantra",
        "Vaiṣṇava Saṃhitā",
        split_items("Ahirbudhnya Samhita|Jayakhya Samhita|Satvata Samhita|Ananda Samhita|Marici Samhita"),
    ),
    (
        "Āgama / Tantra",
        "Śaiva Āgama and Trika Tantra",
        split_items("Kamika Agama|Karana Agama|Suprabheda Agama|Malinivijayottara Tantra|Svacchanda Tantra|Vijnanabhairava Tantra"),
    ),
    (
        "Āgama / Tantra",
        "Śākta / Kaula Tantra",
        split_items("Kularnava Tantra|Mahanirvana Tantra|Yoni Tantra|Rudrayamala Tantra"),
    ),
]


REVIEW_NOTES = {
    "Brihadaranyaka Aranyaka": "Requested label retained; review classification because Bṛhadāraṇyaka is normally catalogued as an Upaniṣad associated with the Śatapatha Brāhmaṇa.",
    "Jabala-Darshana": "Normalized as one Muktika-style title from the supplied separate entries 'Javali' and 'Darshana'; preserve those supplied forms as aliases.",
    "Palani": "Requested spelling retained; identity requires manuscript/catalogue verification before normalization.",
    "Shaundilya": "Likely Śāṇḍilya Upaniṣad; normalize only after authority-file review.",
    "Samnyasa": "Generic or variant title; identify the exact Upaniṣad intended before mirroring.",
    "Dhanurveda Sutra": "Traditional field label may not identify one universally recognized single text; catalogue exact witnesses separately.",
    "Gandharvaveda Sutra": "Traditional field label may not identify one universally recognized single text; catalogue exact witnesses separately.",
    "Shrautasutras": "Corpus-level entry; create recension- and school-specific child records.",
    "Grihyasutras": "Corpus-level entry; create recension- and school-specific child records.",
    "Sulbasutras": "Corpus-level entry; create author/school-specific child records.",
    "Samkhya Sutras": "Traditional attribution to Kapila is historically contested; extant Sāṃkhyapravacana Sūtra is later than classical Sāṃkhya Kārikā.",
    "Uttara Kanda": "Textual history and relationship to the earliest recoverable Rāmāyaṇa layers require edition-specific description.",
    "Harivamsa": "Usually catalogued as a Mahābhārata supplement/khila, not one of its eighteen parvans.",
}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def parent_for(category: str, subgroup: str, title: str) -> str:
    if subgroup == "Rāmāyaṇa" and title != "Ramayana":
        return "Ramayana"
    if subgroup == "Mahābhārata" and title not in {"Mahabharata", "Harivamsa"}:
        return "Mahabharata"
    if category == "Upaniṣad":
        return "Muktika-style 108-title list supplied for this project"
    return ""


def discovery_url(category: str, title: str) -> str:
    query = title.replace(" ", "+")
    if category in {"Itihāsa", "Darśana", "Dharmaśāstra", "Upaveda / Śāstra"}:
        return f"https://github.com/sarit/SARIT-corpus/search?q={query}&type=code"
    return f"https://github.com/INDOLOGY/GRETIL-mirror/search?q={query}&type=code"


def build_rows() -> list[dict[str, str]]:
    rows = []
    seen = Counter()
    for category, subgroup, titles in SECTIONS:
        for title in titles:
            base_id = slugify(f"{category}-{title}")
            seen[base_id] += 1
            record_id = base_id if seen[base_id] == 1 else f"{base_id}-{seen[base_id]}"
            rows.append(
                {
                    "id": record_id,
                    "category": category,
                    "subgroup": subgroup,
                    "title": title,
                    "aliases": "Javali; Darshana" if title == "Jabala-Darshana" else "",
                    "parent_work": parent_for(category, subgroup, title),
                    "attribution": "Traditional/anonymous unless an edition establishes otherwise",
                    "catalog_status": "requested-scope",
                    "mirror_status": "link-only-pending-rights",
                    "commentary_status": "needs-commentary-mapping",
                    "candidate_source": discovery_url(category, title),
                    "review_note": REVIEW_NOTES.get(title, "Verify title normalization, recension, edition, and item-level rights."),
                }
            )
    return rows


def main() -> None:
    CATALOG.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    fieldnames = list(rows[0])
    with (CATALOG / "texts.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    stats = {
        "total_text_records": len(rows),
        "by_category": dict(sorted(Counter(row["category"] for row in rows).items())),
        "generated_from": "scripts/build_catalog.py",
        "scope_note": "This is a requested-scope catalogue, not a claim that every title has a settled canonical status or a reusable digital edition.",
    }
    (CATALOG / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
