from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from .models import NoteFrontMatter, NoteListItem


NOTES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "notes")


def ensure_notes_dir() -> str:
    os.makedirs(NOTES_DIR, exist_ok=True)
    return NOTES_DIR


def _parse_iso8601(value: str) -> datetime:
    v = value.strip()
    # Normalize 'Z' to +00:00 for fromisoformat
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(v)
    except ValueError:
        # Try date only
        dt = datetime.fromisoformat(v + "T00:00:00+00:00")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _parse_list(value: str) -> List[str]:
    v = value.strip()
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"\'') for part in inner.split(",")]
    # fallback single value as list
    return [v]


def parse_front_matter(text: str) -> Tuple[Optional[Dict[str, str]], str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    block = text[4:end]
    content = text[end + 5 :]
    data: Dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        data[key.strip()] = val.strip()
    return data, content


@dataclass
class Note:
    slug: str
    fm: NoteFrontMatter
    content: str


def note_path(slug: str) -> str:
    return os.path.join(ensure_notes_dir(), f"{slug}.md")


def list_note_slugs() -> List[str]:
    ensure_notes_dir()
    slugs = []
    for fname in os.listdir(NOTES_DIR):
        if fname.endswith(".md"):
            slugs.append(os.path.splitext(fname)[0])
    slugs.sort()
    return slugs


def load_note(slug: str) -> Optional[Note]:
    path = note_path(slug)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    fm_raw, content = parse_front_matter(text)
    if fm_raw is None:
        return None
    # map to NoteFrontMatter fields
    title = fm_raw.get("title")
    date_raw = fm_raw.get("date")
    tags_raw = fm_raw.get("tags", "[]")
    summary = fm_raw.get("summary")
    draft_raw = fm_raw.get("draft", "false")
    if not title or not date_raw:
        return None
    fm = NoteFrontMatter(
        title=title,
        date=_parse_iso8601(date_raw),
        tags=_parse_list(tags_raw),
        summary=summary,
        draft=str(draft_raw).lower() in {"1", "true", "yes"},
    )
    return Note(slug=slug, fm=fm, content=content)


def load_all_notes(include_drafts: bool = False) -> List[Note]:
    notes: List[Note] = []
    for slug in list_note_slugs():
        n = load_note(slug)
        if n is None:
            continue
        if not include_drafts and n.fm.draft:
            continue
        notes.append(n)
    notes.sort(key=lambda n: n.fm.date, reverse=True)
    return notes


def to_list_item(note: Note) -> NoteListItem:
    return NoteListItem(
        slug=note.slug,
        title=note.fm.title,
        date=note.fm.date,
        tags=note.fm.tags,
        summary=note.fm.summary,
    )

