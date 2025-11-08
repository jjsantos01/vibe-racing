---
title: Parser ligero de Frontmatter
date: 2025-11-08T11:00:00Z
tags: [markdown, frontmatter]
summary: Implementamos un parser simple de YAML frontmatter sin dependencias.
---

Se evitó traer dependencias externas. El parser soporta claves simples y `tags: [a, b]`. La fecha se parsea en ISO-8601, normalizando el sufijo `Z`.

