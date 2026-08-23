"""
Testes da camada de Retriever.

Objetivo:

    Validar:

    1. Criação do Retriever.
    2. Recuperação semântica.
    3. Geração do embedding da consulta.
    4. Quantidade de resultados.
    5. Ordenação por similaridade.
    6. Preservação dos metadados.
    7. Validação de consultas inválidas.
    8. Validação do parâmetro k.
    9. Comportamento com Vector Store vazio.
"""


import pytest

from vectorstore.embeddings import (
    load_embedding_model,
)

from vectorstore.retriever import (
    Retriever,
    create_retriever,
)

from vectorstore.store import (
    VectorStore,
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="module")
def embedding_model():
    """
    Carrega o modelo de embeddings uma única vez
    durante os testes deste módulo.
    """

    return load_embedding_model()


@pytest.fixture
def vector_store(
    tmp_path,
):
    """
    Cria um Vector Store temporário.

    O Vector Store real do projeto não é alterado.
    """

    path = tmp_path / "index.json"

    return VectorStore(
        path=path,
    )


@pytest.fixture
def documents():
    """
    Cria documentos de teste com embeddings reais.

    Os embeddings são gerados pelo mesmo modelo
    utilizado pelo Retriever.
    """

    return [
        {
            "chunk_id": "chunk_0001",
            "document_id": "doc-001",
            "document_name": "Reforma Tributária",
            "source_organization": "CFC",
            "page": 1,
            "text": (
                "A Reforma Tributária altera "
                "a tributação sobre o consumo."
            ),
        },
        {
            "chunk_id": "chunk_0002",
            "document_id": "doc-001",
            "document_name": "Reforma Tributária",
            "source_organization": "CFC",
            "page": 2,
            "text": (
                "O IVA Dual é composto "
                "pelo IBS e pela CBS."
            ),
        },
        {
            "chunk_id": "chunk_0003",
            "document_id": "doc-002",
            "document_name": "Receita Federal",
            "source_organization": "Receita Federal",
            "page": 3,
            "text": (
                "A transição para o novo sistema "
                "tributário ocorrerá gradualmente."
            ),
        },
    ]


@pytest.fixture
def populated_vector_store(
    vector_store,
    embedding_model,
    documents,
):
    """
    Gera embeddings para os documentos e os adiciona
    ao Vector Store.
    """

    from vectorstore.embeddings import (
        generate_embeddings,
    )

    embedded_documents = generate_embeddings(
        documents,
        embedding_model,
    )

    vector_store.add_documents(
        embedded_documents,
    )

    return vector_store


@pytest.fixture
def retriever(
    populated_vector_store,
    embedding_model,
):
    """
    Cria um Retriever utilizando o Vector Store
    temporário e o modelo de embeddings.
    """

    return Retriever(
        vector_store=populated_vector_store,
        embedding_model=embedding_model,
    )


# ============================================================
# TESTE 1
# ============================================================

def test_create_retriever(
    retriever,
):
    """
    Verifica se o Retriever é criado corretamente.
    """

    assert retriever is not None

    assert retriever.vector_store is not None

    assert retriever.embedding_model is not None


# ============================================================
# TESTE 2
# ============================================================

def test_retrieve(
    retriever,
):
    """
    Verifica a recuperação semântica.
    """

    results = retriever.retrieve(
        "tributação sobre o consumo",
        k=2,
    )

    assert len(results) == 2


# ============================================================
# TESTE 3
# ============================================================

def test_retrieve_returns_relevant_chunk(
    retriever,
):
    """
    Verifica se a consulta recupera o chunk semanticamente
    mais relacionado.
    """

    results = retriever.retrieve(
        "Como funciona a tributação sobre o consumo?",
        k=1,
    )

    assert len(results) == 1

    assert results[0]["chunk_id"] == "chunk_0001"


# ============================================================
# TESTE 4
# ============================================================

def test_retrieve_returns_similarity(
    retriever,
):
    """
    Verifica se os resultados possuem o valor de similaridade.
    """

    results = retriever.retrieve(
        "Reforma Tributária",
        k=2,
    )

    assert len(results) == 2

    assert "similarity" in results[0]

    assert isinstance(
        results[0]["similarity"],
        float,
    )


# ============================================================
# TESTE 5
# ============================================================

def test_retrieve_results_are_ordered(
    retriever,
):
    """
    Verifica se os resultados são retornados em ordem
    decrescente de similaridade.
    """

    results = retriever.retrieve(
        "Reforma Tributária e tributação",
        k=3,
    )

    assert len(results) == 3

    assert results[0]["similarity"] >= (
        results[1]["similarity"]
    )

    assert results[1]["similarity"] >= (
        results[2]["similarity"]
    )


# ============================================================
# TESTE 6
# ============================================================

def test_retrieve_preserves_metadata(
    retriever,
):
    """
    Verifica se os metadados dos documentos são preservados
    durante a recuperação.
    """

    results = retriever.retrieve(
        "tributação sobre o consumo",
        k=1,
    )

    result = results[0]

    assert "chunk_id" in result

    assert "document_id" in result

    assert "document_name" in result

    assert "source_organization" in result

    assert "page" in result

    assert "text" in result

    assert "embedding" in result


# ============================================================
# TESTE 7
# ============================================================

def test_retrieve_empty_query(
    retriever,
):
    """
    Verifica se uma consulta vazia é rejeitada.
    """

    with pytest.raises(ValueError):

        retriever.retrieve(
            "",
        )


# ============================================================
# TESTE 8
# ============================================================

def test_retrieve_whitespace_query(
    retriever,
):
    """
    Verifica se uma consulta contendo apenas espaços
    é rejeitada.
    """

    with pytest.raises(ValueError):

        retriever.retrieve(
            "   ",
        )


# ============================================================
# TESTE 9
# ============================================================

def test_retrieve_invalid_query_type(
    retriever,
):
    """
    Verifica se uma consulta que não é string
    é rejeitada.
    """

    with pytest.raises(TypeError):

        retriever.retrieve(
            123,
        )


# ============================================================
# TESTE 10
# ============================================================

def test_retrieve_invalid_k(
    retriever,
):
    """
    Verifica se k igual a zero é rejeitado.
    """

    with pytest.raises(ValueError):

        retriever.retrieve(
            "Reforma Tributária",
            k=0,
        )


# ============================================================
# TESTE 11
# ============================================================

def test_retrieve_invalid_k_type(
    retriever,
):
    """
    Verifica se k que não é inteiro é rejeitado.
    """

    with pytest.raises(TypeError):

        retriever.retrieve(
            "Reforma Tributária",
            k="5",
        )


# ============================================================
# TESTE 12
# ============================================================

def test_retrieve_empty_vector_store(
    embedding_model,
    tmp_path,
):
    """
    Verifica o comportamento do Retriever quando
    o Vector Store está vazio.
    """

    vector_store = VectorStore(
        path=tmp_path / "empty_index.json",
    )

    retriever = Retriever(
        vector_store=vector_store,
        embedding_model=embedding_model,
    )

    results = retriever.retrieve(
        "Reforma Tributária",
        k=3,
    )

    assert results == []


# ============================================================
# TESTE 13
# ============================================================

def test_create_retriever_factory(
    vector_store,
    embedding_model,
):
    """
    Verifica a função factory create_retriever().
    """

    retriever = create_retriever(
        vector_store=vector_store,
        embedding_model=embedding_model,
    )

    assert isinstance(
        retriever,
        Retriever,
    )

    assert retriever.vector_store is vector_store

    assert retriever.embedding_model is embedding_model

    # ============================================================
# TESTE — FILTRO POR ORGANIZAÇÃO
# ============================================================

def test_filter_results_by_source_organization():

    retriever = object.__new__(Retriever)

    results = [
        {
            "document_name": "documento_1.pdf",
            "source_organization": "CFC",
            "module": "Modulo 1",
        },
        {
            "document_name": "documento_2.pdf",
            "source_organization": "Receita Federal",
            "module": "Modulo 2",
        },
    ]

    filtered = retriever.filter_results(
        results,
        source_organization="CFC",
    )

    assert len(filtered) == 1

    assert filtered[0]["source_organization"] == "CFC"


# ============================================================
# TESTE — FILTRO POR MÓDULO
# ============================================================

def test_filter_results_by_module():

    retriever = object.__new__(Retriever)

    results = [
        {
            "document_name": "documento_1.pdf",
            "source_organization": "CFC",
            "module": "Modulo 1",
        },
        {
            "document_name": "documento_2.pdf",
            "source_organization": "CFC",
            "module": "Modulo 2",
        },
    ]

    filtered = retriever.filter_results(
        results,
        module="Modulo 2",
    )

    assert len(filtered) == 1

    assert filtered[0]["module"] == "Modulo 2"


# ============================================================
# TESTE — FILTRO POR DOCUMENTO
# ============================================================

def test_filter_results_by_document():

    retriever = object.__new__(Retriever)

    results = [
        {
            "document_name": "documento_1.pdf",
            "source_organization": "CFC",
        },
        {
            "document_name": "documento_2.pdf",
            "source_organization": "CFC",
        },
    ]

    filtered = retriever.filter_results(
        results,
        document_name="documento_2.pdf",
    )

    assert len(filtered) == 1

    assert filtered[0]["document_name"] == (
        "documento_2.pdf"
    )


# ============================================================
# TESTE — COMBINAÇÃO DE FILTROS
# ============================================================

def test_filter_results_combined():

    retriever = object.__new__(Retriever)

    results = [
        {
            "document_name": "doc_1.pdf",
            "source_organization": "CFC",
            "module": "Modulo 1",
        },
        {
            "document_name": "doc_2.pdf",
            "source_organization": "CFC",
            "module": "Modulo 2",
        },
        {
            "document_name": "doc_3.pdf",
            "source_organization": "Receita Federal",
            "module": "Modulo 1",
        },
    ]

    filtered = retriever.filter_results(
        results,
        source_organization="CFC",
        module="Modulo 2",
    )

    assert len(filtered) == 1

    assert filtered[0]["document_name"] == (
        "doc_2.pdf"
    )


# ============================================================
# TESTE — SEM FILTROS
# ============================================================

def test_filter_results_without_filters():

    retriever = object.__new__(Retriever)

    results = [
        {
            "document_name": "doc_1.pdf",
            "source_organization": "CFC",
        },
        {
            "document_name": "doc_2.pdf",
            "source_organization": "CFC",
        },
    ]

    filtered = retriever.filter_results(
        results
    )

    assert filtered == results


# ============================================================
# TESTE — RESULTADO VAZIO
# ============================================================

def test_filter_results_empty():

    retriever = object.__new__(Retriever)

    filtered = retriever.filter_results(
        []
    )

    assert filtered == []


# ============================================================
# TESTE — RESULTADOS INVÁLIDOS
# ============================================================

def test_filter_results_invalid_results():

    retriever = object.__new__(Retriever)

    with pytest.raises(TypeError):

        retriever.filter_results(
            "resultado inválido"
        )


# ============================================================
# TESTE — FILTRO INVÁLIDO
# ============================================================

def test_filter_results_invalid_filter():

    retriever = object.__new__(Retriever)

    results = [
        {
            "document_name": "doc.pdf",
            "source_organization": "CFC",
        }
    ]

    with pytest.raises(TypeError):

        retriever.filter_results(
            results,
            source_organization=123,
        )