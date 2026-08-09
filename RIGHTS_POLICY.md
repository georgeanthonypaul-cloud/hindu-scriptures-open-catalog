# Rights and Mirroring Policy

## Governing rule

No file enters `texts/` merely because it is ancient, downloadable, hosted on GitHub, or free to read. The exact digital edition must carry a redistribution permission compatible with public GitHub hosting.

## Required evidence

Each mirrored file must have a row in `catalog/mirror_manifest.csv` containing:

1. a stable upstream URL;
2. title and edition/transcription identity;
3. source organization;
4. license identifier and license URL;
5. required attribution;
6. local destination;
7. SHA-256 checksum after retrieval;
8. verification date and verifier note.

## Allowed statuses

- `approved`: automated download is permitted.
- `pending`: a candidate exists, but edition-level rights are incomplete.
- `link-only`: reading or discovery is allowed; redistribution is not established.
- `blocked`: known copyright or incompatible terms prevent mirroring.

The downloader processes only `approved` rows.

## Layer separation

For every resource, distinguish:

- ancient/root text;
- commentary or subcommentary;
- translation;
- critical apparatus and editorial notes;
- transcription, encoding, or database layer.

Different layers may have different rights. A public-domain Sanskrit work does not erase rights in a recent English translation or TEI transcription.

## Corrections and takedowns

If a rights claim is disputed, open an issue using the rights-review template. Maintainers should set the row to `blocked`, remove the mirrored payload while preserving the catalogue record and provenance, and document the resolution.

This policy is a conservative publication workflow, not legal advice.

