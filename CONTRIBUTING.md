# Contributing

## Add or improve a catalogue record

1. Preserve diacritics where known and add common ASCII spellings as aliases.
2. Identify genre, textual layer, parent work, traditional attribution, and major school associations.
3. Separate base text from commentary, translation, and modern editorial apparatus.
4. Supply a stable source URL and describe whether it is a direct file, catalogue page, or search route.
5. Do not upgrade a record to `approved` without exact edition-level rights evidence.

## Add a mirrored file

Update `catalog/mirror_manifest.csv`, run the fetcher, then run:

```bash
python3 scripts/validate_catalog.py
```

Commit the payload, its generated `.metadata.json`, the manifest update, and any required notice together.

## Commentary contributions

Record the commentator, school, base text, commentary title, approximate period where responsibly known, language, source route, and rights status. Traditional attributions should not be presented as uncontested historical conclusions.

## Conduct

Critique texts and claims directly, but do not demean contributors or religious communities. Evidence, provenance, and clear argument are required; collective blame and personal attacks are not.

