"""
Declarative agent definitions for the BriefScope multi-agent system.

Two roles, each with a system-prompt file and an allow-list of tools:

  ORCHESTRATOR  — talks to the user, searches the project documents itself (RAG),
                  answers directly, and—when a downloadable deliverable is
                  wanted—hands a saved research report to the creator.
                  Tools: RAG search + save/read research + invoke the creator.
  CREATOR       — turns a research report into a downloadable document.
                  Tools: read research + format guide + generate document.

This module is provider-agnostic: nothing here knows about Anthropic, OpenAI,
Google or Ollama. The same definitions drive every plugin variant.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from app import config

_AGENT_PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts" / "agents"


@dataclass(frozen=True)
class AgentDef:
    name: str
    prompt_file: str
    tools: tuple[str, ...]

    @property
    def max_rounds(self) -> int:
        return int(config.get("agent_max_rounds", 8))

    def render_system(
        self,
        *,
        instructions: str = "",
        doc_context: str = "",
        doc_list: str = "",
        guias_tipo: str = "",
    ) -> str:
        """Load the role prompt and inject instructions / document context.

        Uses str.replace (not str.format) so literal braces in the prompt or in
        the injected content never raise KeyError.
        """
        path = _AGENT_PROMPTS_DIR / self.prompt_file
        try:
            template = path.read_text(encoding="utf-8")
        except OSError:
            template = f"You are the {self.name} agent of BriefScope.\n{{instructions}}\n{{doc_context}}"
        return (
            template
            .replace("{instructions}", instructions or "")
            .replace("{doc_context}", doc_context or "")
            .replace("{documentos_disponibles}", doc_list or "")
            .replace("{guias_tipo}", guias_tipo or "")
            .strip()
        )


# Tool names handled specially by the runtime (they spawn sub-agents).
AGENT_INVOCATION_TOOLS = ("invocar_creador_documentos",)

# Search/research tools the orchestrator uses to gather information itself.
RESEARCH_TOOLS = (
    "buscar_en_documentos",
    "guardar_investigacion",
    "leer_investigacion",
    "leer_documento",
)

ORCHESTRATOR = AgentDef(
    name="orquestador",
    prompt_file="orquestador.md",
    tools=RESEARCH_TOOLS + ("invocar_creador_documentos",),
)

CREATOR = AgentDef(
    name="creador",
    prompt_file="creador.md",
    tools=(
        "consultar_guia_formato",
        "consultar_guia_tipo",
        "leer_investigacion",
        "leer_documento",
        "generar_documento_markdown",
        "generar_documento_codigo",
    ),
)

BY_NAME = {a.name: a for a in (ORCHESTRATOR, CREATOR)}
