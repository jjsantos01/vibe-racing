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
- `GET /notes` → array de URLs absolutas a cada nota Markdown (terminadas en `.md`).
- `GET /notes/{slug}.md` → contenido del archivo Markdown original (incluye frontmatter).
- Compat: `GET /notes/{slug}` también sirve el Markdown.

Frontend
--------

- Disponible en `/web` (archivos en `web/`).
- El input acepta el endpoint completo de metadata. Puede tener cualquier nombre (no requiere terminar en `/metadata`).
- Configuración del endpoint:
  - Query param: `?meta=https://api.ejemplo.dev/mi-endpoint` (compat: `?api=`)
  - Variable global antes de `app.js`: `window.DEV_NOTES_METADATA = 'https://api.ejemplo.dev/mi-endpoint'` (compat: `DEV_NOTES_API`)
  - Guardar desde la UI (se persiste en `localStorage`).

Desplegar
---------

- Render Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --proxy-headers`
- Build Command: `pip install -r requirements.txt`

Notas
-----

- El parser de frontmatter es ligero (sin dependencias) y soporta `tags: [a, b]` y fechas ISO-8601 (normaliza `Z`).
- Los borradores (`draft: true`) se omiten en `/notes`.
