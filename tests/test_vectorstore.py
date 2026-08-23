"""
Testes da camada de Vector Store.

Objetivo:

    Validar:

    1. Criação do Vector Store.
    2. Inserção de documentos.
    3. Persistência dos documentos.
    4. Carregamento dos documentos.
    5. Contagem de documentos.
    6. Preservação de texto e metadados.
    7. Busca por similaridade.
    8. Ordenação dos resultados.
    9. Validação de entradas inválidas.
    10. Limpeza do Vector Store.
"""

import pytest

from vectorstore.store import VectorStore


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def vector_store(tmp_path):
    """
    Cria um Vector Store temporário para os testes.

    O uso de tmp_path evita alterar o Vector Store real
    localizado em data/vector_store/.
    """

    path = tmp_path / "index.json"

    return VectorStore(path=path)


@pytest.fixture
def documents():
    """
    Cria documentos de teste com embeddings simples.
    """

    return [
        {
            "chunk_id": "chunk_0001",
            "document_id": "doc-001",
            "document_name": "Documento Reforma Tributária",
            "source_organization": "CFC",
            "page": 1,
            "text": "A Reforma Tributária altera a tributação sobre o consumo.",
            "embedding": [1.0, 0.0, 0.0],
        },
        {
            "chunk_id": "chunk_0002",
            "document_id": "doc-001",
            "document_name": "Documento Reforma Tributária",
            "source_organization": "CFC",
            "page": 2,
            "text": "O IVA Dual é composto pelo IBS e pela CBS.",
            "embedding": [0.0, 1.0, 0.0],
        },
        {
            "chunk_id": "chunk_0003",
            "document_id": "doc-002",
            "document_name": "Documento Receita Federal",
            "source_organization": "Receita Federal",
            "page": 3,
            "text": "A transição para o novo sistema tributário ocorrerá gradualmente.",
            "embedding": [0.0, 0.0, 1.0],
        },
    ]


# ============================================================
# TESTE 1
# ============================================================

def test_create_vector_store(
    vector_store,
):
    """
    Verifica se o Vector Store é criado corretamente.
    """

    assert vector_store is not None

    assert vector_store.count() == 0


# ============================================================
# TESTE 2
# ============================================================

def test_add_documents(
    vector_store,
    documents,
):
    """
    Verifica a inserção de documentos.
    """

    vector_store.add_documents(
        documents
    )

    assert vector_store.count() == 3


# ============================================================
# TESTE 3
# ============================================================

def test_persist_documents(
    vector_store,
    documents,
):
    """
    Verifica se os documentos são persistidos em disco.
    """

    vector_store.add_documents(
        documents
    )

    assert vector_store.path.exists()


# ============================================================
# TESTE 4
# ============================================================

def test_load_persisted_documents(
    vector_store,
    documents,
):
    """
    Verifica se os documentos persistidos podem ser
    carregados por uma nova instância do Vector Store.
    """

    vector_store.add_documents(
        documents
    )

    new_vector_store = VectorStore(
        path=vector_store.path
    )

    assert new_vector_store.count() == 3


# ============================================================
# TESTE 5
# ============================================================

def test_preserve_document_data(
    vector_store,
    documents,
):
    """
    Verifica a preservação do texto e dos metadados.
    """

    vector_store.add_documents(
        documents
    )

    stored_document = vector_store.documents[0]

    assert stored_document["chunk_id"] == "chunk_0001"

    assert stored_document["document_id"] == "doc-001"

    assert stored_document["document_name"] == (
        "Documento Reforma Tributária"
    )

    assert stored_document["source_organization"] == "CFC"

    assert stored_document["page"] == 1

    assert stored_document["text"] == (
        "A Reforma Tributária altera "
        "a tributação sobre o consumo."
    )

    assert stored_document["embedding"] == [
        1.0,
        0.0,
        0.0,
    ]


# ============================================================
# TESTE 6
# ============================================================

def test_similarity_search(
    vector_store,
    documents,
):
    """
    Verifica a busca por similaridade.
    """

    vector_store.add_documents(
        documents
    )

    query_embedding = [
        1.0,
        0.0,
        0.0,
    ]

    results = vector_store.similarity_search(
        query_embedding,
        k=1,
    )

    assert len(results) == 1

    assert results[0]["chunk_id"] == "chunk_0001"


# ============================================================
# TESTE 7
# ============================================================

def test_similarity_search_order(
    vector_store,
    documents,
):
    """
    Verifica se os resultados são ordenados pela
    maior similaridade.
    """

    vector_store.add_documents(
        documents
    )

    query_embedding = [
        0.9,
        0.1,
        0.0,
    ]

    results = vector_store.similarity_search(
        query_embedding,
        k=3,
    )

    assert len(results) == 3

    assert results[0]["chunk_id"] == "chunk_0001"

    assert results[0]["similarity"] >= (
        results[1]["similarity"]
    )

    assert results[1]["similarity"] >= (
        results[2]["similarity"]
    )


# ============================================================
# TESTE 8
# ============================================================

def test_similarity_search_returns_similarity(
    vector_store,
    documents,
):
    """
    Verifica se o resultado contém o valor de similaridade.
    """

    vector_store.add_documents(
        documents
    )

    results = vector_store.similarity_search(
        [1.0, 0.0, 0.0],
        k=1,
    )

    assert "similarity" in results[0]

    assert isinstance(
        results[0]["similarity"],
        float,
    )

    assert results[0]["similarity"] == pytest.approx(
        1.0
    )


# ============================================================
# TESTE 9
# ============================================================

def test_add_documents_invalid_type(
    vector_store,
):
    """
    Verifica se uma entrada inválida é rejeitada.
    """

    with pytest.raises(TypeError):

        vector_store.add_documents(
            "documentos inválidos"
        )


# ============================================================
# TESTE 10
# ============================================================

def test_document_without_embedding(
    vector_store,
):
    """
    Verifica se um documento sem embedding é rejeitado.
    """

    documents = [
        {
            "text": "Documento sem embedding."
        }
    ]

    with pytest.raises(ValueError):

        vector_store.add_documents(
            documents
        )


# ============================================================
# TESTE 11
# ============================================================

def test_document_without_text(
    vector_store,
):
    """
    Verifica se um documento sem texto é rejeitado.
    """

    documents = [
        {
            "embedding": [1.0, 0.0, 0.0]
        }
    ]

    with pytest.raises(ValueError):

        vector_store.add_documents(
            documents
        )


# ============================================================
# TESTE 12
# ============================================================

def test_similarity_search_empty_store(
    vector_store,
):
    """
    Verifica o comportamento da busca em um Vector Store vazio.
    """

    results = vector_store.similarity_search(
        [1.0, 0.0, 0.0],
        k=3,
    )

    assert results == []


# ============================================================
# TESTE 13
# ============================================================

def test_similarity_search_invalid_k(
    vector_store,
):
    """
    Verifica se k inválido é rejeitado.
    """

    with pytest.raises(ValueError):

        vector_store.similarity_search(
            [1.0, 0.0, 0.0],
            k=0,
        )


# ============================================================
# TESTE 14
# ============================================================

def test_similarity_search_dimension_mismatch(
    vector_store,
    documents,
):
    """
    Verifica se embeddings com dimensões diferentes
    são rejeitados.
    """

    vector_store.add_documents(
        documents
    )

    with pytest.raises(ValueError):

        vector_store.similarity_search(
            [1.0, 0.0],
            k=1,
        )


# ============================================================
# TESTE 15
# ============================================================

def test_clear_vector_store(
    vector_store,
    documents,
):
    """
    Verifica se o Vector Store pode ser limpo.
    """

    vector_store.add_documents(
        documents
    )

    assert vector_store.count() == 3

    vector_store.clear()

    assert vector_store.count() == 0

    assert not vector_store.path.exists()