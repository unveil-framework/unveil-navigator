#!/usr/bin/env python3
"""Generate Markdown docs and repository URLs for UNVEIL tactics/techniques."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


DEFAULT_REPO_BASE_URL = "https://github.com/UNVEILFramework/unveil-navigator/blob/main"
PAGE_NOISE_RE = re.compile(r"Page\s+\d+\s+of\s+\d+", re.IGNORECASE)
BOOK_HEADER_RE = re.compile(r"The Art and Science of Virtual HUMINT \(2024\)", re.IGNORECASE)
TACTIC_HEADING_RE = re.compile(r"^\d+\s+(UTA\d{2})\s+(.+?)\s*$")
TECHNIQUE_HEADING_RE = re.compile(r"^UT\d{4}(?:\.\d{3})?\s*-")


def slug(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def clean_description(text: str) -> str:
    text = PAGE_NOISE_RE.sub("", text)
    text = BOOK_HEADER_RE.sub("", text)
    text = text.replace("\f", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def markdown(text: str) -> str:
    return clean_description(text).replace("\n\n", "\n\n").strip()


def load_bundle(path: Path) -> tuple[list[dict], list[dict]]:
    objects = json.loads(path.read_text(encoding="utf-8"))["objects"]
    tactics = [obj for obj in objects if obj.get("type") == "x-mitre-tactic"]
    techniques = [obj for obj in objects if obj.get("type") == "attack-pattern"]
    return tactics, techniques


def external_id(obj: dict) -> str:
    return obj["external_references"][0]["external_id"]


def load_enrichments(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data if isinstance(data, list) else data["techniques"]
    return {entry["techniqueID"]: entry for entry in entries}


def tactic_shortname(tactic: dict) -> str:
    return tactic["x_mitre_shortname"]


def tactic_display_name(tactic: dict) -> str:
    tactic_id = external_id(tactic)
    name = tactic["name"]
    return name.removeprefix(f"{tactic_id} - ").strip()


def technique_display_name(technique: dict) -> str:
    return technique["name"].strip()


def docs_relative_path(path: Path, docs_root: Path) -> str:
    return path.relative_to(docs_root).as_posix()


def repo_url(repo_base_url: str, path: Path) -> str:
    return f"{repo_base_url.rstrip('/')}/{path.as_posix()}"


def extract_tactic_descriptions(book_text_path: Path) -> dict[str, str]:
    if not book_text_path.exists():
        return {}

    lines = book_text_path.read_text(encoding="utf-8", errors="replace").splitlines()
    descriptions: dict[str, str] = {}
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        match = TACTIC_HEADING_RE.match(line)
        if not match:
            index += 1
            continue

        tactic_id = match.group(1)
        body: list[str] = []
        index += 1
        while index < len(lines):
            current = lines[index].strip()
            if TECHNIQUE_HEADING_RE.match(current) or TACTIC_HEADING_RE.match(current):
                break
            if current and not PAGE_NOISE_RE.match(current) and not BOOK_HEADER_RE.match(current):
                body.append(current)
            elif body and body[-1] != "":
                body.append("")
            index += 1

        description = clean_description("\n".join(body))
        if description:
            descriptions[tactic_id] = description

    return descriptions


def technique_docs_path(docs_root: Path, tactic: dict, technique: dict) -> Path:
    tactic_id = external_id(tactic)
    tactic_name = tactic_display_name(tactic)
    technique_id = external_id(technique)
    technique_name = technique_display_name(technique)
    return (
        docs_root
        / "tactics"
        / f"{tactic_id}-{slug(tactic_name)}"
        / f"{technique_id}-{slug(technique_name)}.md"
    )


def tactic_docs_path(docs_root: Path, tactic: dict) -> Path:
    tactic_id = external_id(tactic)
    tactic_name = tactic_display_name(tactic)
    return docs_root / "tactics" / f"{tactic_id}-{slug(tactic_name)}" / "README.md"


def write_docs(
    docs_root: Path,
    tactics: list[dict],
    techniques: list[dict],
    enrichments: dict[str, dict],
    tactic_descriptions: dict[str, str],
) -> dict[str, Path]:
    if docs_root.exists():
        shutil.rmtree(docs_root)
    docs_root.mkdir(parents=True)

    technique_by_phase: dict[str, list[dict]] = {}
    for technique in techniques:
        for phase in technique.get("kill_chain_phases", []):
            if phase.get("kill_chain_name") == "unveil":
                technique_by_phase.setdefault(phase["phase_name"], []).append(technique)

    doc_paths: dict[str, Path] = {}

    index_lines = [
        "# UNVEIL Framework Documentation",
        "",
        "Generated from the local UNVEIL Navigator bundle and book-derived technique descriptions.",
        "",
        "## Tactics",
        "",
    ]

    for tactic in sorted(tactics, key=external_id):
        tactic_id = external_id(tactic)
        tactic_name = tactic_display_name(tactic)
        tactic_path = tactic_docs_path(docs_root, tactic)
        tactic_path.parent.mkdir(parents=True, exist_ok=True)
        doc_paths[tactic_id] = tactic_path

        tactic_techniques = sorted(technique_by_phase.get(tactic_shortname(tactic), []), key=external_id)
        description = tactic_descriptions.get(tactic_id) or tactic.get("description", "")

        lines = [
            f"# {tactic_id} - {tactic_name}",
            "",
            "## Description",
            "",
            markdown(description),
            "",
            "## Techniques",
            "",
        ]

        for technique in tactic_techniques:
            technique_id = external_id(technique)
            technique_name = technique_display_name(technique)
            technique_path = technique_docs_path(docs_root, tactic, technique)
            lines.append(f"- [{technique_id} - {technique_name}](./{technique_path.name})")
            doc_paths.setdefault(technique_id, technique_path)

        tactic_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        index_lines.append(f"- [{tactic_id} - {tactic_name}]({docs_relative_path(tactic_path, docs_root)})")

        for technique in tactic_techniques:
            technique_id = external_id(technique)
            technique_name = technique_display_name(technique)
            technique_path = technique_docs_path(docs_root, tactic, technique)
            enrichment = enrichments.get(technique_id, {})
            description = enrichment.get("description") or technique.get("description", "")

            technique_lines = [
                f"# {technique_id} - {technique_name}",
                "",
                f"**Tactic:** [{tactic_id} - {tactic_name}](./README.md)",
                "",
                "## Description",
                "",
                markdown(description),
                "",
            ]
            technique_path.write_text("\n".join(technique_lines).rstrip() + "\n", encoding="utf-8")

    (docs_root / "README.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    return doc_paths


def update_urls(
    bundle_path: Path,
    enrichment_path: Path,
    docs_root: Path,
    repo_base_url: str,
    doc_paths: dict[str, Path],
) -> None:
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    for obj in bundle["objects"]:
        if obj.get("type") not in {"x-mitre-tactic", "attack-pattern"}:
            continue
        item_id = external_id(obj)
        if item_id not in doc_paths:
            continue
        obj["external_references"][0]["url"] = repo_url(repo_base_url, doc_paths[item_id])
    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")

    enrichment = json.loads(enrichment_path.read_text(encoding="utf-8"))
    entries = enrichment if isinstance(enrichment, list) else enrichment["techniques"]
    for entry in entries:
        technique_id = entry["techniqueID"]
        if technique_id in doc_paths:
            entry["url"] = repo_url(repo_base_url, doc_paths[technique_id])
    enrichment_path.write_text(json.dumps(enrichment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_no_pdf_noise(docs_root: Path, enrichment_path: Path) -> None:
    files = list(docs_root.rglob("*.md")) + [enrichment_path]
    offenders = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        if PAGE_NOISE_RE.search(text) or BOOK_HEADER_RE.search(text):
            offenders.append(path)
    if offenders:
        formatted = "\n".join(str(path) for path in offenders)
        raise SystemExit(f"PDF extraction noise found in generated docs:\n{formatted}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=Path("nav-app/src/assets/data/latest.json"))
    parser.add_argument(
        "--enrichment",
        type=Path,
        default=Path("nav-app/src/assets/data/unveil-technique-descriptions.json"),
    )
    parser.add_argument("--docs-root", type=Path, default=Path("docs/unveil-framework"))
    parser.add_argument(
        "--book-text",
        type=Path,
        default=Path("../unveil-stix-data/input/Apuntes Cyberhumint(3).text"),
    )
    parser.add_argument("--repo-base-url", default=DEFAULT_REPO_BASE_URL)
    args = parser.parse_args()

    tactics, techniques = load_bundle(args.bundle)
    enrichments = load_enrichments(args.enrichment)
    tactic_descriptions = extract_tactic_descriptions(args.book_text)
    doc_paths = write_docs(args.docs_root, tactics, techniques, enrichments, tactic_descriptions)
    update_urls(args.bundle, args.enrichment, args.docs_root, args.repo_base_url, doc_paths)
    validate_no_pdf_noise(args.docs_root, args.enrichment)

    print(f"Generated docs for {len(tactics)} tactics and {len(techniques)} techniques in {args.docs_root}")
    print(f"Updated URLs in {args.bundle} and {args.enrichment}")


if __name__ == "__main__":
    main()
