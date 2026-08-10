#!/usr/bin/env python3
"""Search the Hindu Scriptures Open Catalogue and optionally mirrored full text."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


DEFAULT_REPO = Path("/Users/gappaul/Documents/web app/hindu-scriptures-open-catalog")
CATALOGS = ("texts.csv", "commentaries.csv", "sources.csv", "mirror_manifest.csv")


def find_repo(explicit: str | None) -> Path:
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    candidates.extend([Path.cwd(), *Path.cwd().parents, DEFAULT_REPO])
    for candidate in candidates:
        if (candidate / "catalog" / "mirror_manifest.csv").is_file():
            return candidate.resolve()
    raise SystemExit("Repository not found. Pass --repo /path/to/hindu-scriptures-open-catalog")


def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def catalogue_matches(repo: Path, terms: list[str]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for name in CATALOGS:
        path = repo / "catalog" / name
        with path.open(encoding="utf-8", newline="") as handle:
            for row_number, row in enumerate(csv.DictReader(handle), start=2):
                haystack = normalized(" ".join(row.values()))
                if all(term in haystack for term in terms):
                    results.append({"catalog": name, "row": row_number, "record": row})
    return results


def text_matches(repo: Path, terms: list[str], limit: int) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for path in sorted((repo / "texts").rglob("*")):
        if not path.is_file() or path.name.endswith(".metadata.json") or path.name == "README.md":
            continue
        try:
            with path.open(encoding="utf-8", errors="replace") as handle:
                for line_number, line in enumerate(handle, start=1):
                    if all(term in normalized(line) for term in terms):
                        results.append({
                            "path": str(path.relative_to(repo)),
                            "line": line_number,
                            "excerpt": re.sub(r"\s+", " ", line).strip()[:500],
                        })
                        if len(results) >= limit:
                            return results
        except OSError:
            continue
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Words that must all occur in a matching record or line")
    parser.add_argument("--repo", help="Path to the catalogue repository")
    parser.add_argument("--full-text", action="store_true", help="Also search mirrored TXT/XML payloads")
    parser.add_argument("--limit", type=int, default=25, help="Maximum full-text matches (default: 25)")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of readable text")
    args = parser.parse_args()

    repo = find_repo(args.repo)
    terms = [normalized(term) for term in args.query.split() if normalized(term)]
    if not terms:
        raise SystemExit("Query must contain at least one non-space character")

    data = {
        "query": args.query,
        "repository": str(repo),
        "catalogue_matches": catalogue_matches(repo, terms),
        "full_text_matches": text_matches(repo, terms, max(1, args.limit)) if args.full_text else [],
        "warning": "Search hits are leads. Verify the cited edition, bibliographic data, quotation, and locator before writing a Chicago citation.",
    }

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print(f"Repository: {repo}")
    print(f"Query: {args.query}")
    print(f"Catalogue matches: {len(data['catalogue_matches'])}")
    for match in data["catalogue_matches"]:
        record = match["record"]
        title = record.get("title") or record.get("work_title") or record.get("name") or record.get("id") or "(untitled)"
        print(f"- {match['catalog']}:{match['row']} — {title}")
        for key in ("id", "school", "scholar", "source_url", "license_id", "destination", "rights_status", "mirror_status"):
            if record.get(key):
                print(f"  {key}: {record[key]}")
    if args.full_text:
        print(f"Full-text matches: {len(data['full_text_matches'])}")
        for match in data["full_text_matches"]:
            print(f"- {match['path']}:{match['line']} — {match['excerpt']}")
    print(data["warning"])


if __name__ == "__main__":
    main()
