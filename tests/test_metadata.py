"""
Testes do módulo Metadata.

Objetivo:

    Validar se o gerenciamento de metadados consegue:

    1. Criar metadata padronizado.
    2. Aceitar metadata válido.
    3. Rejeitar metadata que não seja um dicionário.
    4. Validar campos obrigatórios.
    5. Permitir campos opcionais.
    6. Preservar os valores informados.
"""

import pytest

from ingestion.metadata import (
    DOCUMENT_METADATA_FIELDS,
    create_document_metadata,
    validate_document_metadata,
)


# ============================================================
# METADATA DE TESTE
# ============================================================

VALID_METADATA = {
    "document_id": "test-document-001",
    "document_name": "Documento de Teste",
    "document_type": "PDF",
    "source_organization": "CFC",
    "publication_date": "2026-07-29",
    "source_url": "https://www.gov.br/",
}


# ============================================================
# TESTE 1
# ============================================================

def test_document_metadata_fields():
    """
    Verifica se todos os campos esperados de metadata
    estão definidos.
    """

    expected_fields = {
        "document_id",
        "document_name",
        "document_type",
        "source_organization",
        "publication_date",
        "source_url",
    }

    assert DOCUMENT_METADATA_FIELDS == expected_fields


# ============================================================
# TESTE 2
# ============================================================

def test_validate_valid_metadata():
    """
    Verifica se metadata válido é aceito.
    """

    result = validate_document_metadata(
        VALID_METADATA
    )

    assert result is None


# ============================================================
# TESTE 3
# ============================================================

def test_create_document_metadata():
    """
    Verifica a criação de metadata padronizado.
    """

    metadata = create_document_metadata(
        document_id="test-document-001",
        document_name="Documento de Teste",
        document_type="PDF",
        source_organization="CFC",
        publication_date="2026-07-29",
        source_url="https://www.gov.br/",
    )

    assert metadata == VALID_METADATA


# ============================================================
# TESTE 4
# ============================================================

def test_optional_metadata_fields():
    """
    Verifica se publication_date e source_url
    podem ser omitidos.
    """

    metadata = create_document_metadata(
        document_id="test-document-002",
        document_name="Documento sem dados opcionais",
        document_type="PDF",
        source_organization="CFC",
    )

    assert metadata["publication_date"] is None
    assert metadata["source_url"] is None


# ============================================================
# TESTE 5
# ============================================================

def test_missing_document_id():
    """
    Verifica se document_id é obrigatório.
    """

    metadata = VALID_METADATA.copy()
    metadata.pop("document_id")

    with pytest.raises(
        ValueError,
        match="document_id",
    ):
        validate_document_metadata(metadata)


# ============================================================
# TESTE 6
# ============================================================

def test_missing_document_name():
    """
    Verifica se document_name é obrigatório.
    """

    metadata = VALID_METADATA.copy()
    metadata.pop("document_name")

    with pytest.raises(
        ValueError,
        match="document_name",
    ):
        validate_document_metadata(metadata)


# ============================================================
# TESTE 7
# ============================================================

def test_missing_document_type():
    """
    Verifica se document_type é obrigatório.
    """

    metadata = VALID_METADATA.copy()
    metadata.pop("document_type")

    with pytest.raises(
        ValueError,
        match="document_type",
    ):
        validate_document_metadata(metadata)


# ============================================================
# TESTE 8
# ============================================================

def test_missing_source_organization():
    """
    Verifica se source_organization é obrigatório.
    """

    metadata = VALID_METADATA.copy()
    metadata.pop("source_organization")

    with pytest.raises(
        ValueError,
        match="source_organization",
    ):
        validate_document_metadata(metadata)


# ============================================================
# TESTE 9
# ============================================================

def test_invalid_metadata_type():
    """
    Verifica se metadata precisa ser um dicionário.
    """

    with pytest.raises(
        TypeError,
        match="metadata deve ser um dicionário",
    ):
        validate_document_metadata(
            "metadata inválido"
        )


# ============================================================
# TESTE 10
# ============================================================

def test_empty_required_metadata_field():
    """
    Verifica se campos obrigatórios não podem
    possuir valores vazios.
    """

    metadata = VALID_METADATA.copy()
    metadata["document_name"] = ""

    with pytest.raises(
        ValueError,
        match="document_name",
    ):
        validate_document_metadata(metadata)