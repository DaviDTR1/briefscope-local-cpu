# Changelog

All notable changes to **BriefScope LOCAL CPU** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-06-14

First public release as a QueAI plugin.

### Added

- Document-analysis agent over user-uploaded documents (PDF, DOCX, XLSX, TXT,
  MD and more), organized into projects.
- Retrieval strategy that adapts to corpus size: full-context for small
  corpora, RAG (ChromaDB vector search) above a configurable token threshold.
- Multi-agent orchestration (orchestrator + creator) for research and
  deliverable generation.
- Downloadable file generation in two engines:
  - **Rapid mode** (Markdown → DOCX via pandoc, → PDF via WeasyPrint, → HTML).
  - **Code mode** (Python: reportlab / python-docx / python-pptx / openpyxl)
    for PDF, DOCX, PPTX and XLSX with precise layout.
- Streaming chat responses (SSE) with conversation history and automatic
  history compaction to save tokens.
- React frontend with a Spanish/English language switcher.
- Settings UI to choose the Ollama model and the local embedding model, and to
  tune RAG / history parameters; configuration persists to `data/config.json`.
- User-selectable local embedding model (sentence-transformers), with
  recommended models documented in `.env.example`.
- QueAI integration: `manifest.json`, Traefik `PathPrefix` routing, healthcheck
  endpoint, and bundled Ollama + ChromaDB services via `docker-compose.yml`.

### Notes

- Runs **fully offline on CPU**: LLM via a bundled Ollama container, embeddings
  in-process via sentence-transformers. No API keys or internet required after
  the model and embedding weights are downloaded on first use.
- Changing the embedding model invalidates previously indexed documents — they
  must be re-uploaded so they are re-embedded with the new model.

[Unreleased]: https://github.com/queai-project/QueAI
[1.0.0]: https://github.com/queai-project/QueAI
