"""
Testes do Pipeline de ingestão documental.

Fluxo validado:

    PDF
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
"""

from pathlib import Path

import pytest

from ingestion.pipeline import process_document


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "documentos"
    / "Modulo_1_parte_1.pdf"
)


# ============================================================
# METADATA DE TESTE
# ============================================================

DOCUMENT_ID = "test-pipeline-001"
DOCUMENT_NAME = "Modulo 1 - Reforma Tributária"
DOCUMENT_TYPE = "PDF"
SOURCE_ORGANIZATION = "CFC"


# ============================================================
# TESTE 1
# ============================================================

def test_process_document():
    """
    Verifica se o Pipeline processa o PDF completo.
    """

    result = process_document(
        file_path=PDF_PATH,
        document_id=DOCUMENT_ID,
        document_name=DOCUMENT_NAME,
        document_type=DOCUMENT_TYPE,
        source_organization=SOURCE_ORGANIZATION,
    )

    assert isinstance(result, dict)

    assert result["metadata"]["document_id"] == DOCUMENT_ID

    assert result["extraction"]["pages_extracted"] == 63

    assert result["cleaning"]["pages_cleaned"] == 63

    assert result["chunking"]["chunk_count"] > 0


# ============================================================
# TESTE 2
# ============================================================

def test_pipeline_result_structure():
    """
    Verifica a estrutura do resultado do Pipeline.
    """

    result = process_document(
        file_path=PDF_PATH,
        document_id=DOCUMENT_ID,
        document_name=DOCUMENT_NAME,
        document_type=DOCUMENT_TYPE,
        source_organization=SOURCE_ORGANIZATION,
    )

    assert "metadata" in result
    assert "extraction" in result
    assert "cleaning" in result
    assert "chunking" in result
    assert "statistics" in result


# ============================================================
# TESTE 3
# ============================================================

def test_pipeline_statistics():
    """
    Verifica se as estatísticas refletem o processamento.
    """

    result = process_document(
        file_path=PDF_PATH,
        document_id=DOCUMENT_ID,
        document_name=DOCUMENT_NAME,
        document_type=DOCUMENT_TYPE,
        source_organization=SOURCE_ORGANIZATION,
    )

    statistics = result["statistics"]

    assert statistics["pages_extracted"] == 63

    assert statistics["pages_cleaned"] == 63

    assert statistics["chunks_created"] > 0


# ============================================================
# TESTE 4
# ============================================================

def test_pipeline_metadata():
    """
    Verifica se os metadados são propagados até o resultado.
    """

    result = process_document(
        file_path=PDF_PATH,
        document_id=DOCUMENT_ID,
        document_name=DOCUMENT_NAME,
        document_type=DOCUMENT_TYPE,
        source_organization=SOURCE_ORGANIZATION,
        publication_date="2026-07-29",
        source_url="https://www.gov.br/",
    )

    metadata = result["metadata"]

    assert metadata["document_id"] == DOCUMENT_ID

    assert metadata["document_name"] == DOCUMENT_NAME

    assert metadata["document_type"] == DOCUMENT_TYPE

    assert metadata["source_organization"] == SOURCE_ORGANIZATION

    assert metadata["publication_date"] == "2026-07-29"

    assert metadata["source_url"] == "https://www.gov.br/"


# ============================================================
# TESTE 5
# ============================================================

def test_pipeline_chunks_contain_metadata():
    """
    Verifica se os chunks recebem os metadados documentais.
    """

    result = process_document(
        file_path=PDF_PATH,
        document_id=DOCUMENT_ID,
        document_name=DOCUMENT_NAME,
        document_type=DOCUMENT_TYPE,
        source_organization=SOURCE_ORGANIZATION,
    )

    chunks = result["chunking"]["chunks"]

    assert len(chunks) > 0

    first_chunk = chunks[0]

    assert first_chunk["document_id"] == DOCUMENT_ID

    assert first_chunk["document_name"] == DOCUMENT_NAME

    assert first_chunk["document_type"] == DOCUMENT_TYPE

    assert first_chunk["source_organization"] == SOURCE_ORGANIZATION


# ============================================================
# TESTE 6
# ============================================================

def test_pipeline_invalid_file():
    """
    Verifica se o Pipeline propaga o erro quando
    o arquivo não existe.
    """

    invalid_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "documentos"
        / "arquivo_inexistente.pdf"
    )

    with pytest.raises(FileNotFoundError):
        process_document(
            file_path=invalid_path,
            document_id=DOCUMENT_ID,
            document_name=DOCUMENT_NAME,
            document_type=DOCUMENT_TYPE,
            source_organization=SOURCE_ORGANIZATION,
        )