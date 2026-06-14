# Format guide: PDF

There are **two paths** to produce a PDF. Choose based on visual complexity.

## Fast path — `generar_documento_markdown` (recommended by default)
Write the document in **Markdown** and the engine converts it to PDF (Markdown → HTML → PDF with WeasyPrint). Supports full Unicode, tables, lists, quotes, code and **your own CSS**.

Contract:
- `formato`: `"pdf"`
- `contenido_markdown`: the document in Markdown.
- `nombre_archivo`: without extension, only letters/numbers/hyphens.
- `estilo_css` (optional): full CSS rules (`@page`, `body`, `h1`, `table`...). If you omit it, a default professional style is applied (A4, clean typography, tables with a colored header).

Use it for reports, memos, documentation, proposals and any document that is structured text. For a branded finish, pass your own `estilo_css`.

Common mistakes to avoid:
- Do not include the `<html>` or `<style>` block: only Markdown (and optionally CSS separately in `estilo_css`).
- Markdown tables need the separator row `|---|---|`.
- For CSS page breaks use `page-break-before: always;` on a selector.

## Code path — `generar_documento_codigo`
Only if you need **pixel-perfect control**: certificates, absolute positioning, vector graphics, cover pages with full-bleed images. You write Python with **reportlab**.

Contract:
- `formato`: `"pdf"`
- `codigo_python`: script that builds the PDF. You have `OUTPUT_PATH` (destination path) and the helper `guardar_documento(obj)`. With reportlab you usually write directly to `OUTPUT_PATH`.
- `nombre_archivo`: without extension.

Minimal example:
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
c.setFont("Helvetica-Bold", 24)
c.drawString(72, 760, "Title")
c.showPage()
c.save()
```

Common mistakes:
- Remember to call `c.save()` (or `doc.build(...)` with platypus) or the file will be empty.
- reportlab coordinates have their origin at the bottom-left.
- For long styled text use `platypus` (SimpleDocTemplate + Paragraph), not `drawString`.

**Quick decision:** is it structured text? → fast path. Is it custom design? → code path.
