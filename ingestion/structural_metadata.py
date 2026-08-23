"""
Identificação de metadados estruturais do documento.

Responsabilidade:

    Identificar contexto estrutural das páginas, como:

        - módulo;
        - seção;
        - tópico.

Esta etapa ocorre após a limpeza e antes do chunking.

Fluxo:

    Documento limpo
        ↓
    Structural Metadata
        ↓
    Páginas contextualizadas
        ↓
    Chunking
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


# ============================================================
# IDENTIFICAÇÃO DO MÓDULO
# ============================================================

def extract_module_from_filename(
    filename: str | Path,
) -> str | None:
    """
    Identifica o módulo a partir do nome do arquivo.

    Exemplos:

        Modulo_11_parte_2.PDF
            → Módulo 11

        Modulo_1_parte_1.pdf
            → Módulo 1
    """

    filename = Path(filename).name

    match = re.search(
        r"modulo[_\s-]*(\d+)",
        filename,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    return f"Módulo {match.group(1)}"


# ============================================================
# IDENTIFICAÇÃO DE TÍTULOS
# ============================================================

def is_structural_heading(
    text: str,
) -> bool:
    """
    Identifica possíveis títulos/seções.

    Utiliza heurísticas simples para documentos
    institucionais e materiais didáticos.
    """

    text = text.strip()

    if not text:
        return False

    if len(text) > 120:
        return False

    if text.endswith(
        (".", ";", ":", ",")
    ):
        return False

    words = text.split()

    if len(words) > 15:
        return False

    letters = [
        char
        for char in text
        if char.isalpha()
    ]

    if not letters:
        return False

    uppercase_ratio = (
        sum(
            char.isupper()
            for char in letters
        )
        / len(letters)
    )

    return uppercase_ratio >= 0.70


# ============================================================
# ESTRUTURAÇÃO DE UMA PÁGINA
# ============================================================

def enrich_document_structure(
    document: list[dict[str, Any]],
    document_name: str,
) -> list[dict[str, Any]]:
    """
    Enriquece as páginas com contexto estrutural.

    O módulo é identificado pelo nome do documento.

    A seção é identificada pelos títulos encontrados
    no conteúdo das páginas.

    O último contexto conhecido é propagado para
    páginas seguintes.
    """

    module = extract_module_from_filename(
        document_name
    )

    enriched_document: list[dict[str, Any]] = []

    current_section: str | None = None

    for page in document:

        page_copy = dict(page)

        text = page_copy.get(
            "text",
            "",
        )

        # ----------------------------------------------------
        # Identificação da seção
        # ----------------------------------------------------

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        page_headings = [
            line
            for line in lines
            if is_structural_heading(line)
        ]

        # ----------------------------------------------------
        # Primeiro título estrutural encontrado
        # ----------------------------------------------------

        if page_headings:
            current_section = page_headings[0]

        page_copy["module"] = module
        page_copy["section"] = current_section
        page_copy["topic"] = None

        enriched_document.append(
            page_copy
        )

    return enriched_document