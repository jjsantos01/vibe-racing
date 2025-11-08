Dev Notes API (Vibe Racing)
===========================

Backend en FastAPI para notas de desarrollo descentralizadas, con:

- Endpoint de metadata conforme a `schema-profile.json` (`/metadata`).
- Lista de notas (`/notes`).
- Detalle de nota en Markdown con frontmatter (`/notes/{slug}`).

Estructura
----------

- `app/main.py`: aplicación FastAPI.
- `app/models.py`: modelos Pydantic (metadata y notas).
- `app/notes.py`: utilidades para cargar y parsear notas.
- `data/notes`: 5 notas de ejemplo `.md` con frontmatter.

Ejecutar localmente
-------------------

1. Crear entorno y dependencias:
   `pip install -r requirements.txt`
2. Correr API:
   `uvicorn app.main:app --reload`
3. Docs: `http://localhost:8000/docs`

Endpoints
---------

- `GET /metadata` → objeto JSON con datos del perfil y `fileList.url` apuntando a `/notes`.
- `GET /notes` → lista tipada de notas (slug, title, date, tags, summary).
- `GET /notes/{slug}` → contenido del archivo Markdown original (incluye frontmatter).

Notas
-----

- El parser de frontmatter es ligero (sin dependencias) y soporta `tags: [a, b]` y fechas ISO-8601 (normaliza `Z`).
- Los borradores (`draft: true`) se omiten en `/notes`.

