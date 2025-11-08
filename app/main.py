from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from .models import FileList, NotesListResponse, Profile, ProfileMetadata
from .notes import load_all_notes, load_note, note_path, to_list_item


app = FastAPI(title="Vibe Racing Dev Notes API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True, "ts": datetime.now(tz=timezone.utc).isoformat()}


@app.get("/metadata", response_model=ProfileMetadata)
def get_metadata(request: Request) -> ProfileMetadata:
    base = str(request.base_url).rstrip("/")
    notes_url = f"{base}/notes"
    return ProfileMetadata(
        version="1.0.0",
        profile=Profile(
            name="Vibe Racer",
            avatar="https://avatars.githubusercontent.com/u/583231?v=4",
            contact={
                "github": "vibe-racer",
                "linkedin": "https://www.linkedin.com/",
                "email": "viberacer@example.com",
                "twitter": "@vibe_racer",
                "website": f"{base}",
                "other": [
                    {
                        "platform": "Docs",
                        "url": f"{base}/docs",
                        "label": "API Docs",
                    }
                ],
            },
        ),
        fileList=FileList(
            url=notes_url,
            format="json",
            lastUpdated=datetime.now(tz=timezone.utc),
        ),
    )


@app.get("/notes", response_model=NotesListResponse)
def list_notes() -> NotesListResponse:
    notes = load_all_notes(include_drafts=False)
    items = [to_list_item(n) for n in notes]
    return NotesListResponse(count=len(items), items=items)


@app.get("/notes/{slug}", response_class=PlainTextResponse)
def get_note(slug: str):
    note = load_note(slug)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    # Return the raw file content including frontmatter
    # We read again from disk to preserve original formatting/frontmatter
    with open(note_path(slug), "r", encoding="utf-8") as f:
        content = f.read()
    return PlainTextResponse(content, media_type="text/markdown; charset=utf-8")

