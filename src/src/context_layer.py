"""LLM context layer demo: ingest -> extract -> validate -> share.

Synthetic data only. Run: python3 src/context_layer.py
"""

import json
import re
from pathlib import Path

from config import ACCESS_LIST, WORK_KEYWORDS

DATA = Path(__file__).resolve().parent.parent / "data"


def ingest_chat_export(path):
    """Format A: JSON chat export. Different LLMs export differently; each
    format gets its own adapter so the rest of the pipeline sees one shape."""
    raw = json.loads(Path(path).read_text())
    owner = raw["owner"]
    items = [m["text"] for m in raw["messages"] if m["role"] == "assistant"]
    return owner, items


def ingest_markdown_export(path):
    """Format B: Markdown notes with Work/Personal sections."""
    text = Path(path).read_text()
    owner = re.search(r"owner:\s*(\w+)", text).group(1)
    work_section = text.split("## Work", 1)[1].split("## Personal", 1)[0]
    items = [line.lstrip("- ").strip() for line in work_section.splitlines() if line.startswith("-")]
    return owner, items


def is_work_relevant(item):
    """Step 1 of the real work: select the right context, skip personal noise."""
    lowered = item.lower()
    return any(kw in lowered for kw in WORK_KEYWORDS)


def validate_against_db(item, known_projects):
    """Step 2: check context against the internal database before sharing.
    Items referencing unknown projects are quarantined, not shared."""
    mentioned = re.findall(r"Project\s+\w+", item)
    unknown = [p for p in mentioned if p not in known_projects]
    return (len(unknown) == 0, unknown)


def shareable_items(owner, items, known_projects):
    validated, quarantined = [], []
    for item in items:
        if not is_work_relevant(item):
            continue
        ok, unknown = validate_against_db(item, known_projects)
        (validated if ok else quarantined).append((item, unknown))
    return validated, quarantined


def main():
    known_projects = json.loads((DATA / "project_db.json").read_text())["projects"]

    sources = [
        ingest_chat_export(DATA / "llm_export_chat.json"),
        ingest_markdown_export(DATA / "notes_export.md"),
    ]

    digests = {}   # recipient -> list of (owner, item)
    quarantine = []  # (owner, item, unknown_projects)

    for owner, items in sources:
        validated, quarantined = shareable_items(owner, items, known_projects)
        quarantine.extend((owner, item, unknown) for item, unknown in quarantined)
        for recipient in ACCESS_LIST.get(owner, []):
            digests.setdefault(recipient, []).extend((owner, item) for item, _ in validated)

    print("=== Per-recipient digests (validated, access-permitted) ===")
    for recipient, entries in sorted(digests.items()):
        print(f"\n{recipient} receives:")
        for owner, item in entries:
            print(f"  - [{owner}] {item}")

    print("\n=== Quarantine (failed validation - NOT shared) ===")
    for owner, item, unknown in quarantine:
        print(f"  - [{owner}] {item}  (unknown: {', '.join(unknown)})")


if __name__ == "__main__":
    main()
