from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
import httpx
from urllib.parse import urlparse
import ipaddress, socket

from pydantic import AnyHttpUrl

from .models import FileList, Profile, ProfileMetadata
from .notes import load_all_notes, load_note, note_path


app = FastAPI(title="Vibe Racing Dev Notes API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static frontend mounted at /web
import os

WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
if os.path.isdir(WEB_DIR):
    app.mount("/web", StaticFiles(directory=WEB_DIR, html=True), name="web")


@app.get("/", include_in_schema=False)
def index_root():
    index_path = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Dev Notes API. Frontend en /web"}


def _is_public_hostname(host: str) -> bool:
    try:
        if host in {"localhost"}:
            return False
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        addrs = []
        for info in infos:
            sockaddr = info[4] if len(info) >= 5 else None
            if not sockaddr:
                continue
            addr = sockaddr[0]
            if addr:
                addrs.append(addr)
        if not addrs:
            return False
        for addr in addrs:
            try:
                ip = ipaddress.ip_address(addr)
            except ValueError:
                return False
            # Only allow globally routable IPs
            if not ip.is_global:
                return False
        return True
    except Exception:
        return False


@app.get("/proxy")
async def proxy(url: str, request: Request):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise HTTPException(status_code=400, detail="Unsupported scheme")
    if not parsed.hostname or not _is_public_hostname(parsed.hostname):
        raise HTTPException(status_code=400, detail="Blocked host")
    accept = request.headers.get("accept", "*/*")
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            r = await client.get(url, headers={"Accept": accept})
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")
    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/octet-stream"),
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


@app.get("/notes", response_model=List[AnyHttpUrl])
def list_notes(request: Request) -> List[AnyHttpUrl]:
    base = str(request.base_url).rstrip("/")
    notes = load_all_notes(include_drafts=False)
    urls: List[str] = [f"{base}/notes/{n.slug}.md" for n in notes]
    return urls


@app.get("/notes/{slug}", response_class=PlainTextResponse)
def get_note(slug: str):
    # Allow slugs that include the .md extension
    if slug.endswith(".md"):
        slug = slug[:-3]
    note = load_note(slug)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    # Return the raw file content including frontmatter
    # We read again from disk to preserve original formatting/frontmatter
    with open(note_path(slug), "r", encoding="utf-8") as f:
        content = f.read()
    return PlainTextResponse(content, media_type="text/markdown; charset=utf-8")


@app.get("/notes/{slug}.md", response_class=PlainTextResponse)
def get_note_md(slug: str):
    return get_note(slug)
