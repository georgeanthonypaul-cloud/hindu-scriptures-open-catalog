---
name: research-hindu-sources-chicago
description: Search, verify, quote, analyze, critique, or write about Hindu scriptures, commentaries, schools, gurus, Dharmaśāstra, caste, varna, Vedānta, Nyāya, Vaiśeṣika, Sāṃkhya, Yoga, Mīmāṃsā, Purāṇas, epics, Vedas, Upaniṣads, Āgamas, Tantras, and related traditions using the Hindu Scriptures Open Catalogue. Use for source-based Hinduism research, apologetics, historical analysis, textual comparison, fact-checking, quotations, bibliographies, footnotes, and Chicago-style citations. Require edition-level bibliographic verification and never invent authors, translators, editors, page numbers, publication data, quotations, or canonical locators.
---

# Research Hindu Sources with Chicago Citations

Use the Hindu Scriptures Open Catalogue as the first research corpus. Treat every root text, commentary, translation, edition, transcription, and website as a distinct bibliographic object.

## Required references

Read [references/corpus-routing.md](references/corpus-routing.md) before searching the corpus.

Read [references/citation-standard.md](references/citation-standard.md) before quoting or citing any source. Follow its Chicago notes-bibliography templates and verification rules.

When the task critiques Hinduism or caste, also invoke `$evaluate-hinduism-from-george-framework` and `$reformed-periyar-critique-method`. This skill supplies sources and citations; those skills govern the interpretive and rhetorical framework.

## Research workflow

1. Identify the exact proposition, passage, doctrine, text layer, commentary, school, and historical period at issue.
2. Search the local catalogue and verified mirror first. Run:

   ```bash
   python3 scripts/search_corpus.py "QUERY"
   ```

   From an installed skill, pass `--repo /absolute/path/to/hindu-scriptures-open-catalog` when automatic discovery fails.
3. Read the matching catalogue row, mirror-manifest row, metadata sidecar, and the relevant source text. For TEI/XML, inspect the complete `teiHeader`, especially `fileDesc`, `titleStmt`, `publicationStmt`, `sourceDesc`, `availability`, and `revisionDesc`.
4. Verify the actual edition. Record author or traditional attribution, full title, commentator, translator, editor, volume, edition, publication place, publisher, year, stable URL or repository, license, and access date as applicable.
5. Verify the locator against the cited edition. Use a printed page only when the scan or digital edition preserves stable pagination. Otherwise use the work’s canonical locator—book, kāṇḍa, parvan, chapter, verse, sūtra, brāhmaṇa, section, or hymn—and identify the digital edition.
6. Check every quotation character by character against the cited edition. If quoting a translation, name its translator. If translating Sanskrit directly, label it “author’s translation” or “my translation” and cite the Sanskrit edition.
7. Compare rival witnesses before presenting “the Hindu view.” Separate Śruti, Smṛti, epic, Purāṇa, Dharmaśāstra, philosophical sūtra, commentary, sectarian text, regional practice, and modern interpretation.
8. Cite every material textual or historical claim. Give a full Chicago note on first mention, shortened notes thereafter, and a bibliography when the genre permits.
9. State limitations. Mark OCR uncertainty, partial editions, missing pages, disputed attribution, recension differences, reconstructed text, and unresolved rights or publication data.

## Non-negotiable citation rule

Do not output a polished citation until the cited copy itself supports the bibliographic fields and locator. Never infer a page number from a search-result position, PDF viewer counter, OCR line, Project Gutenberg line, or another edition.

When a stable printed page is unavailable, do not manufacture one to satisfy a request for pages. Use a canonical locator and explain that the digital edition is unpaginated. If the user requires a page number, locate a paginated scan of the same edition or say that the page remains unverified.

## Source hierarchy

Prefer, in order:

1. the verified mirrored edition and its adjacent metadata;
2. a scan of the edition’s title page, copyright/publication page, and cited page;
3. the publisher, library, archive, or scholarly project record;
4. a critical edition or established scholarly translation;
5. secondary scholarship for interpretation and historical context;
6. discovery pages only as leads, never as proof.

Do not treat availability, GitHub hosting, an open-source code license, ancient authorship, or an uploader’s description as proof that a modern edition or translation is reusable.

## Output requirements

For each substantive source, provide:

- the exact passage or claim supported;
- text and canonical locator;
- author or traditional attribution;
- commentator, translator, and editor where applicable;
- edition, volume, publication place, publisher, and year where available;
- stable page number from that edition, or a clearly identified canonical locator when unpaginated;
- full Chicago note on first citation;
- shortened Chicago note on later citations;
- Chicago bibliography entry;
- edition or OCR limitations that affect confidence.

Keep citations attached to the claims they support. Do not cite the catalogue as a substitute for citing the underlying book or edition.

## Final audit

Before delivery, confirm that:

- every quoted word appears in the cited edition;
- every page number belongs to that exact edition;
- every translation names its translator;
- commentarial claims identify the commentator and school;
- traditional attribution is not presented as settled modern authorship;
- canonical locators and printed pages are not confused;
- the bibliography and notes agree on title, edition, publisher, and year;
- no discovery-only or rights-unclear file has been silently treated as reusable;
- competing textual witnesses and the strongest relevant interpretation have been represented fairly;
- uncertainty is stated instead of repaired by invention.
