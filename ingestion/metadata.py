"""
Gerenciamento de metadados documentais.

Responsabilidades:

    1. Definir os campos obrigatórios de metadata.
    2. Validar metadata documental.
    3. Criar metadata padronizado para documentos.
"""

from typing import Any


# ============================================================
# CAMPOS DE METADATA
# ============================================================

DOCUMENT_METADATA_FIELDS = {
    "document_id",
    "document_name",
    "document_type",
    "source_organization",
    "publication_date",
    "source_url",
}


# ============================================================
# VALIDAÇÃO
# ============================================================

def validate_document_metadata(
    metadata: dict[str, Any],
) -> None:
    """
    Valida os metadados obrigatórios de um documento.

    Parameters
    ----------
    metadata:
        Dicionário contendo os metadados documentais.

    Raises
    ------
    TypeError
        Quando metadata não é um dicionário.

    ValueError
        Quando algum campo obrigatório está ausente.
    """

    if not isinstance(metadata, dict):
        raise TypeError(
            "metadata deve ser um dicionário."
        )

    required_fields = DOCUMENT_METADATA_FIELDS - {
        "publication_date",
        "source_url",
    }

    for field in required_fields:
        if not metadata.get(field):
            raise ValueError(
                f"Metadado obrigatório ausente: {field}"
            )


# ============================================================
# CRIAÇÃO
# ============================================================

def create_document_metadata(
    document_id: str,
    document_name: str,
    document_type: str,
    source_organization: str,
    publication_date: str | None = None,
    source_url: str | None = None,
) -> dict[str, Any]:
    """
    Cria metadata documental padronizado.
    """

    metadata = {
        "document_id": document_id,
        "document_name": document_name,
        "document_type": document_type,
        "source_organization": source_organization,
        "publication_date": publication_date,
        "source_url": source_url,
    }

    validate_document_metadata(metadata)

    return metadata