"""
Testes da camada de Embeddings.

Objetivo:

    Validar:

    1. Carregamento do modelo.
    2. Geração de embedding.
    3. Validação de texto.
    4. Geração de embeddings para chunks.
    5. Preservação dos metadados.
"""


import pytest

from vectorstore.embeddings import (
    DEFAULT_EMBEDDING_MODEL,
    load_embedding_model,
    generate_embedding,
    generate_embeddings,
)


# ============================================================
# FIXTURE
# ============================================================

@pytest.fixture(scope="module")
def embedding_model():
    """
    Carrega o modelo uma única vez para os testes.
    """

    return load_embedding_model(
        DEFAULT_EMBEDDING_MODEL
    )


# ============================================================
# TESTE 1
# ============================================================

def test_load_embedding_model(
    embedding_model,
):
    """
    Verifica se o modelo é carregado corretamente.
    """

    assert embedding_model is not None


# ============================================================
# TESTE 2
# ============================================================

def test_generate_embedding(
    embedding_model,
):
    """
    Verifica a geração de um embedding.
    """

    text = (
        "A Reforma Tributária altera "
        "a tributação sobre o consumo."
    )

    embedding = generate_embedding(
        text,
        embedding_model,
    )

    assert isinstance(
        embedding,
        list,
    )

    assert len(embedding) > 0

    assert all(
        isinstance(value, float)
        for value in embedding
    )


# ============================================================
# TESTE 3
# ============================================================

def test_generate_embedding_empty_text(
    embedding_model,
):
    """
    Verifica se texto vazio é rejeitado.
    """

    with pytest.raises(ValueError):

        generate_embedding(
            "",
            embedding_model,
        )


# ============================================================
# TESTE 4
# ============================================================

def test_generate_embedding_invalid_text(
    embedding_model,
):
    """
    Verifica se texto inválido é rejeitado.
    """

    with pytest.raises(TypeError):

        generate_embedding(
            123,
            embedding_model,
        )


# ============================================================
# TESTE 5
# ============================================================

def test_generate_embeddings(
    embedding_model,
):
    """
    Verifica a geração de embeddings para múltiplos chunks.
    """

    chunks = [

        {
            "chunk_id": "chunk_0001",
            "document_id": "doc-001",
            "page": 1,
            "text": (
                "A Reforma Tributária "
                "institui novos tributos."
            ),
        },

        {
            "chunk_id": "chunk_0002",
            "document_id": "doc-001",
            "page": 2,
            "text": (
                "O IVA Dual possui "
                "características específicas."
            ),
        },

    ]

    result = generate_embeddings(
        chunks,
        embedding_model,
    )

    assert len(result) == 2

    assert "embedding" in result[0]

    assert "embedding" in result[1]


# ============================================================
# TESTE 6
# ============================================================

def test_embeddings_preserve_metadata(
    embedding_model,
):
    """
    Verifica se os metadados dos chunks são preservados.
    """

    chunks = [

        {
            "chunk_id": "chunk_0001",
            "document_id": "doc-001",
            "document_name": "Documento Teste",
            "source_organization": "CFC",
            "page": 10,
            "text": "Conteúdo sobre Reforma Tributária.",
        }

    ]

    result = generate_embeddings(
        chunks,
        embedding_model,
    )

    embedded_chunk = result[0]

    assert embedded_chunk["chunk_id"] == "chunk_0001"

    assert embedded_chunk["document_id"] == "doc-001"

    assert embedded_chunk["document_name"] == "Documento Teste"

    assert embedded_chunk["source_organization"] == "CFC"

    assert embedded_chunk["page"] == 10

    assert embedded_chunk["text"] == (
        "Conteúdo sobre Reforma Tributária."
    )

    assert "embedding" in embedded_chunk