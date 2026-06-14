# Format guide: HTML

A single path: **`generar_documento_markdown`** with `formato: "html"`.

Write the document in **Markdown** and the engine wraps it in a self-contained, styled HTML5 page (a single file, no external dependencies).

Contract:
- `formato`: `"html"`
- `contenido_markdown`: the document in Markdown (tables, lists, code with basic highlighting, quotes).
- `nombre_archivo`: without extension.
- `estilo_css` (optional): full CSS that replaces the default style. Use it for brand colors, typography or your own layout. If you omit it, a clean professional style is applied.

Use it for standalone pages, browsable reports, fact sheets or any deliverable to be viewed in a browser.

Common mistakes:
- Do not wrap the content in `<html>`/`<body>`: the engine already generates the full page. Pass only Markdown.
- If you want your own CSS it goes **entirely** in `estilo_css`, not embedded in the Markdown.
- Markdown tables require the separator row `|---|---|`.

For PDF from the same content, use `formato: "pdf"` (same engine, same CSS).
