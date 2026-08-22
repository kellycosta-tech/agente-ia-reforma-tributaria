"""
Pipeline de processamento documental.

Responsabilidade:

    Orquestrar as etapas de ingestão documental:

        Documento
            ↓
        Extraction
            ↓
        Cleaning
            ↓
        Metadata
            ↓
        Chunking
            ↓
        Resultado estruturado

O Pipeline não implementa a lógica das etapas.
Ele apenas coordena os módulos especializados.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ingestion.chunking import chunk_document
from ingestion.cleaning import clean_document
from ingestion.extraction import extract_document
from ingestion.metadata import create_document_metadata


# ============================================================
# PIPELINE
# ============================================================

def process_document(
    file_path: str | Path,
    document_id: str,
    document_name: str,
    document_type: str,
    source_organization: str,
    publication_date: str | None = None,
    source_url: str | None = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> dict[str, Any]:
    """
    Processa um documento através do pipeline de ingestão.

    Fluxo:

        Extraction
            ↓
        Cleaning
            ↓
        Metadata
            ↓
        Chunking

    Parameters
    ----------
    file_path:
        Caminho do documento.

    document_id:
        Identificador único do documento.

    document_name:
        Nome do documento.

    document_type:
        Tipo do documento, por exemplo PDF.

    source_organization:
        Organização responsável pela publicação.

    publication_date:
        Data de publicação, quando disponível.

    source_url:
        URL oficial da fonte, quando disponível.

    chunk_size:
        Tamanho aproximado dos chunks.

    chunk_overlap:
        Sobreposição entre chunks.

    Returns
    -------
    dict[str, Any]
        Resultado estruturado do processamento.

    Raises
    ------
    FileNotFoundError
        Quando o documento não existe.
    """

    # ========================================================
    # 1. EXTRACTION
    # ========================================================

    extracted_document = extract_document(
        file_path
    )

    # ========================================================
    # 2. CLEANING
    # ========================================================

    cleaned_document = clean_document(
        extracted_document
    )

    # ========================================================
    # 3. METADATA
    # ========================================================

    document_metadata = create_document_metadata(
        document_id=document_id,
        document_name=document_name,
        document_type=document_type,
        source_organization=source_organization,
        publication_date=publication_date,
        source_url=source_url,
    )

    # ========================================================
    # 4. CHUNKING
    # ========================================================

    chunks = chunk_document(
        cleaned_document,
        document_metadata=document_metadata,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # ========================================================
    # 5. RESULTADO
    # ========================================================

    return {
        "metadata": document_metadata,

        "extraction": {
            "pages_extracted": len(
                extracted_document
            ),
        },

        "cleaning": {
            "pages_cleaned": len(
                cleaned_document
            ),
        },

        "chunking": {
            "chunks": chunks,
            "chunk_count": len(chunks),
        },

        "statistics": {
            "pages_extracted": len(
                extracted_document
            ),
            "pages_cleaned": len(
                cleaned_document
            ),
            "chunks_created": len(chunks),
        },
    }