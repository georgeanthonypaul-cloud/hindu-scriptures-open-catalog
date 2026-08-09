# Hindu Scriptures Open Catalogue

An open, provenance-first catalogue of Hindu scriptures, commentaries, historical editions, and reusable digital texts.

## Project status

This repository is a catalogue first and a mirror second. It records the full requested scope even when a legally reusable digital edition has not yet been verified. A text is copied into `texts/` only after its exact digital edition, attribution, source, and redistribution license have been checked.

Current scope includes:

- the four Vedas and their Saṃhitā, Brāhmaṇa, and Āraṇyaka layers;
- the 108 Upaniṣads in the supplied Muktikā-style list;
- the Rāmāyaṇa, Mahābhārata, their major divisions, Bhagavad Gītā, and Harivaṃśa;
- the eighteen Mahāpurāṇas and the requested Upapurāṇas;
- Dharmaśāstras, Dharmasūtras, Vedāṅgas, Upavedas, Darśana sūtras, Āgamas, and Tantras;
- commentarial traditions and the thirty scholars specified in the original research request.

The current machine-readable release contains 248 requested-scope text records, including exactly 108 normalized Upaniṣad records, plus 44 initial author/commentary mappings. “All commentaries” is an open-ended scholarly objective rather than a finite completed set; coverage growth is tracked explicitly instead of being falsely declared complete.

## What “open” means here

| Status | Repository treatment |
|---|---|
| Public domain or CC0 | May be mirrored after edition-level verification |
| CC BY / CC BY-SA | May be mirrored with attribution and license obligations |
| Free to read | Link only unless redistribution permission is explicit |
| Open-source code | Does not automatically license embedded scripture data |
| Unknown or mixed | Catalogue entry only; do not mirror |

Ancient authorship does **not** make a modern translation, critical edition, transcription, database, or typesetting public domain.

## Repository map

- `catalog/texts.csv` — requested scriptures and structural components
- `catalog/commentaries.csv` — scholars, commentaries, and text relationships
- `catalog/sources.csv` — source registries and reuse policies
- `catalog/mirror_manifest.csv` — exact files approved for automated mirroring
- `texts/` — downloaded open-license files, grouped by source and license
- `scripts/fetch_open_resources.py` — checksum-aware, allowlist-only downloader
- `scripts/validate_catalog.py` — catalogue and license validation
- `RIGHTS_POLICY.md` — mandatory rights workflow
- `THIRD_PARTY_NOTICES.md` — attribution for mirrored material

## Quick start

```bash
python3 scripts/validate_catalog.py
python3 scripts/fetch_open_resources.py --dry-run
python3 scripts/fetch_open_resources.py
```

## Research discipline

Root text, commentary, translation, and editorial apparatus are distinct works. The catalogue therefore records relationships rather than silently treating one school’s commentary as the meaning of the base text. Traditional authorship is reported as traditional attribution where historical authorship is composite, anonymous, or disputed.

## Contributing

Pull requests are welcome. Every proposed mirror must include an exact source URL, edition information, named rights holder where applicable, SPDX-style license identifier, required attribution, and a checksum. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licensing

- Project code: MIT, see [LICENSE](LICENSE).
- Original catalogue metadata: CC0-1.0, see [DATA_LICENSE.md](DATA_LICENSE.md).
- Third-party texts: each retains its own license and attribution. See its adjacent metadata and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

This project is not affiliated with or endorsed by SARIT, Ambuda, GRETIL, Sanskrit Documents, Muktabodha, Gita Supersite, or any other listed host.
