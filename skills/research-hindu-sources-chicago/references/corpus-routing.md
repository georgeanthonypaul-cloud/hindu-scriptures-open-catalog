# Hindu Corpus Routing

## Corpus location

Primary repository: `https://github.com/georgeanthonypaul-cloud/hindu-scriptures-open-catalog`

Default local repository: `/Users/gappaul/Documents/web app/hindu-scriptures-open-catalog`

Resolve the repository in this order:

1. explicit `--repo` argument;
2. current working directory or its parents containing `catalog/mirror_manifest.csv`;
3. the default local repository above;
4. the public GitHub repository.

## Search surfaces

- `catalog/texts.csv`: 248 requested scripture and component records, including the normalized 108-Upaniṣad list.
- `catalog/commentaries.csv`: scholar, school, work, and text relationships.
- `catalog/sources.csv`: repositories and rights/access descriptions.
- `catalog/mirror_manifest.csv`: exact approved downloads, source URLs, licenses, attribution, verification notes, repository destinations, and SHA-256 values.
- `catalog/COVERAGE.md`: current coverage and named gaps.
- `texts/**`: mirrored Sanskrit, TEI/XML, English translations, and commentaries.
- `texts/**/*.metadata.json`: provenance and rights sidecars.
- `THIRD_PARTY_NOTICES.md`: corpus-level attribution.
- `RIGHTS_POLICY.md`: redistribution rules.

## Current verified mirror

The current manifest contains 29 files:

- 14 SARIT Sanskrit/TEI files under CC BY-SA 3.0 or 4.0;
- 2 Ambuda/DCS Sanskrit epics under CC BY 4.0;
- 11 Project Gutenberg books identified as public domain in the United States;
- 2 Internet Archive OCR texts based on nineteenth-century Upaniṣad volumes.

Coverage is edition-specific. The mirror currently supplies at least partial Sanskrit or English coverage for 53 catalogue records. The remaining records are discovery routes until an exact reusable edition is verified.

## Search sequence

1. Search titles, normalized titles, alternate spellings, schools, commentators, translators, and work IDs with `scripts/search_corpus.py`.
2. Inspect matching rows in all catalogue CSVs.
3. For an approved mirror, open the manifest destination and adjacent `.metadata.json` file.
4. For TEI/XML, search the header before the body:
   - `<titleStmt>` for title, author, editor, and responsibility;
   - `<publicationStmt>` and `<availability>` for digital publication and license;
   - `<sourceDesc>` or `<bibl>` for the source edition;
   - `<revisionDesc>` for version history;
   - `<pb>` for preserved printed pagination.
5. For Project Gutenberg, inspect the title/credits block and original publication information. Treat the ebook number and Gutenberg release as digital-host data, not automatically as the original edition statement.
6. For Internet Archive OCR, verify the title page and cited printed page in the scan. OCR text alone does not establish pagination or exact spelling.
7. For Ambuda/DCS, cite the work’s canonical locator and the DCS/Ambuda digital corpus. Do not invent print-page data for a machine-readable corpus.
8. If bibliographic fields remain incomplete, follow the source URL to the host record or locate a paginated scan of the same edition before citing.

## Canonical locator preference

- Veda: maṇḍala–sūkta–verse or kāṇḍa/prapāṭhaka/anuvāka as appropriate to the recension.
- Brāhmaṇa/Āraṇyaka/Upaniṣad: book/chapter/section/verse used by the cited edition.
- Bhagavad Gītā: chapter.verse.
- Mahābhārata: parvan, chapter, verse; identify the edition because numbering differs.
- Rāmāyaṇa: kāṇḍa, sarga, verse; identify recension and edition.
- Purāṇa: book or khaṇḍa, chapter, verse; identify recension/edition.
- Dharmaśāstra: chapter.verse or sūtra/section.
- Darśana: adhyāya/pāda/sūtra or the edition’s accepted sūtra number.
- Tantra/Āgama: chapter and verse/section used by the edition.
- Commentary: root-text locator plus commentary title and commentator; add commentary page if preserved.

Never assume locator systems match across editions.

## Rights boundary

The user’s permission covers original repository code and catalogue metadata. It cannot relicense third-party editions. Cite free-to-read and rights-unclear materials when lawful, but do not copy substantial protected text or upload it as reusable data without a verified license or public-domain basis.
