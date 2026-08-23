"""
Testes da camada RAG.

Valida a integração entre:

    RAG
     ↓
    Retriever
     ↓
    Vector Store

E também valida:

    Chunks recuperados
          ↓
    Montagem do contexto
          ↓
    Metadados de origem
"""


import pytest

from app.rag import (
    RAG,
    create_rag,
)


# ============================================================
# MOCK RETRIEVER
# ============================================================


class FakeRetriever:

    def retrieve(
        self,
        query,
        k=5,
        source_organization=None,
        module=None,
        document_name=None,
    ):

        return [
            {
                "chunk_id": "chunk_0001",
                "document_id": "doc_001",
                "document_name": "Modulo_1_parte_1.pdf",
                "source_organization": "CFC",
                "page": 10,
                "section": "Introdução",
                "text": "Conteúdo sobre Reforma Tributária.",
                "similarity": 0.95,
            }
        ][:k]


# ============================================================
# TESTE 1
# ============================================================


def test_create_rag():

    rag = RAG(
        retriever=FakeRetriever()
    )

    assert rag is not None


# ============================================================
# TESTE 2
# ============================================================


def test_create_rag_invalid_retriever():

    with pytest.raises(TypeError):

        RAG(
            retriever=None
        )


# ============================================================
# TESTE 3
# ============================================================


def test_retrieve():

    rag = object.__new__(RAG)

    rag.retriever = FakeRetriever()

    results = rag.retrieve(
        "O que é a Reforma Tributária?"
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) == 1


# ============================================================
# TESTE 4
# ============================================================


def test_retrieve_preserves_metadata():

    rag = object.__new__(RAG)

    rag.retriever = FakeRetriever()

    results = rag.retrieve(
        "O que é a Reforma Tributária?"
    )

    result = results[0]

    assert result["chunk_id"] == "chunk_0001"

    assert result["document_id"] == "doc_001"

    assert result["document_name"] == (
        "Modulo_1_parte_1.pdf"
    )

    assert result["source_organization"] == "CFC"

    assert result["page"] == 10

    assert result["section"] == "Introdução"

    assert "text" in result


# ============================================================
# TESTE 5
# ============================================================


def test_retrieve_empty_query():

    rag = object.__new__(RAG)

    rag.retriever = FakeRetriever()

    with pytest.raises(ValueError):

        rag.retrieve("")


# ============================================================
# TESTE 6
# ============================================================


def test_retrieve_invalid_query():

    rag = object.__new__(RAG)

    rag.retriever = FakeRetriever()

    with pytest.raises(TypeError):

        rag.retrieve(123)


# ============================================================
# TESTE 7
# ============================================================


def test_retrieve_invalid_k():

    rag = object.__new__(RAG)

    rag.retriever = FakeRetriever()

    with pytest.raises(ValueError):

        rag.retrieve(
            "Reforma Tributária",
            k=0,
        )


# ============================================================
# TESTE 8
# ============================================================


def test_retrieve_invalid_k_type():

    rag = object.__new__(RAG)

    rag.retriever = FakeRetriever()

    with pytest.raises(TypeError):

        rag.retrieve(
            "Reforma Tributária",
            k="5",
        )


# ============================================================
# TESTE 9
# ============================================================


def test_build_context():

    rag = object.__new__(RAG)

    results = [
        {
            "chunk_id": "chunk_0001",
            "document_id": "doc_001",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 10,
            "section": "Introdução",
            "text": "Conteúdo sobre Reforma Tributária.",
        }
    ]

    context = rag.build_context(
        results
    )

    assert isinstance(
        context,
        str,
    )

    assert "Conteúdo sobre Reforma Tributária." in context


# ============================================================
# TESTE 10
# ============================================================


def test_build_context_preserves_document():

    rag = object.__new__(RAG)

    results = [
        {
            "chunk_id": "chunk_0001",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 10,
            "section": "Introdução",
            "text": "Conteúdo sobre Reforma Tributária.",
        }
    ]

    context = rag.build_context(
        results
    )

    assert "Modulo_1_parte_1.pdf" in context


# ============================================================
# TESTE 11
# ============================================================


def test_build_context_preserves_source():

    rag = object.__new__(RAG)

    results = [
        {
            "chunk_id": "chunk_0001",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 10,
            "text": "Conteúdo sobre Reforma Tributária.",
        }
    ]

    context = rag.build_context(
        results
    )

    assert "CFC" in context


# ============================================================
# TESTE 12
# ============================================================


def test_build_context_preserves_page():

    rag = object.__new__(RAG)

    results = [
        {
            "chunk_id": "chunk_0001",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 10,
            "text": "Conteúdo sobre Reforma Tributária.",
        }
    ]

    context = rag.build_context(
        results
    )

    assert "Página: 10" in context


# ============================================================
# TESTE 13
# ============================================================


def test_build_context_multiple_chunks():

    rag = object.__new__(RAG)

    results = [
        {
            "chunk_id": "chunk_0001",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 10,
            "text": "Primeiro conteúdo.",
        },
        {
            "chunk_id": "chunk_0002",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 11,
            "text": "Segundo conteúdo.",
        },
    ]

    context = rag.build_context(
        results
    )

    assert "Primeiro conteúdo." in context

    assert "Segundo conteúdo." in context

    assert "[TRECHO 1]" in context

    assert "[TRECHO 2]" in context


# ============================================================
# TESTE 14
# ============================================================


def test_build_context_empty_results():

    rag = object.__new__(RAG)

    context = rag.build_context(
        []
    )

    assert context == ""


# ============================================================
# TESTE 15
# ============================================================


def test_build_context_invalid_result():

    rag = object.__new__(RAG)

    with pytest.raises(TypeError):

        rag.build_context(
            [
                "resultado inválido"
            ]
        )


# ============================================================
# TESTE 16
# ============================================================

def test_build_context():

    rag = object.__new__(RAG)

    results = [
        {
            "chunk_id": "chunk_0001",
            "document_id": "doc_001",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 10,
            "text": "Conteúdo sobre Reforma Tributária.",
            "similarity": 0.95,
        }
    ]

    context = rag.build_context(
        results
    )

    assert isinstance(
        context,
        str,
    )

    assert "Modulo_1_parte_1.pdf" in context

    assert "CFC" in context

    assert "10" in context

    assert "Conteúdo sobre Reforma Tributária." in context


# ============================================================
# TESTE 17
# ============================================================

def test_build_context_preserves_metadata():

    rag = object.__new__(RAG)

    results = [
        {
            "chunk_id": "chunk_0001",
            "document_id": "doc_001",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 10,
            "section": "Introdução",
            "text": "Conteúdo sobre Reforma Tributária.",
            "similarity": 0.95,
        }
    ]

    context = rag.build_context(
        results
    )

    assert "Modulo_1_parte_1.pdf" in context

    assert "CFC" in context

    assert "Página: 10" in context

    assert "Seção: Introdução" in context

    assert "Conteúdo sobre Reforma Tributária." in context


# ============================================================
# TESTE 18
# ============================================================

def test_build_context_multiple_chunks():

    rag = object.__new__(RAG)

    results = [
        {
            "chunk_id": "chunk_0001",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 10,
            "text": "Primeiro conteúdo.",
        },
        {
            "chunk_id": "chunk_0002",
            "document_name": "Modulo_1_parte_2.pdf",
            "source_organization": "Receita Federal",
            "page": 20,
            "text": "Segundo conteúdo.",
        },
    ]

    context = rag.build_context(
        results
    )

    assert "[Fonte 1]" in context

    assert "[Fonte 2]" in context

    assert "Primeiro conteúdo." in context

    assert "Segundo conteúdo." in context

    assert "Modulo_1_parte_1.pdf" in context

    assert "Modulo_1_parte_2.pdf" in context


# ============================================================
# TESTE 19
# ============================================================

def test_build_context_empty_results():

    rag = object.__new__(RAG)

    context = rag.build_context(
        []
    )

    assert context == ""


# ============================================================
# TESTE 20
# ============================================================

def test_build_context_invalid_results():

    rag = object.__new__(RAG)

    with pytest.raises(TypeError):

        rag.build_context(
            "resultado inválido"
        )


# ============================================================
# TESTE 21
# ============================================================

def test_build_context_invalid_result_item():

    rag = object.__new__(RAG)

    with pytest.raises(TypeError):

        rag.build_context(
            [
                "resultado inválido"
            ]
        )


# ============================================================
# TESTE 22
# ============================================================

def test_build_context_invalid_text():

    rag = object.__new__(RAG)

    results = [
        {
            "document_name": "documento.pdf",
            "source_organization": "CFC",
            "page": 10,
            "text": 123,
        }
    ]

    with pytest.raises(TypeError):

        rag.build_context(
            results
        )


# ============================================================
# TESTE 23
# ============================================================

def test_retrieve_context():

    rag = RAG(
        retriever=FakeRetriever()
    )

    result = rag.retrieve_context(
        "O que é a Reforma Tributária?"
    )

    assert isinstance(
        result,
        dict,
    )

    assert result["query"] == (
        "O que é a Reforma Tributária?"
    )

    assert isinstance(
        result["results"],
        list,
    )

    assert isinstance(
        result["context"],
        str,
    )

    assert "Reforma Tributária" in (
        result["context"]
    )

    assert "Modulo_1_parte_1.pdf" in (
        result["context"]
    )

    assert "Página: 10" in (
        result["context"]
    )

# ============================================================
# TESTE 17 — FILTRO POR ORGANIZAÇÃO
# ============================================================

def test_retrieve_with_source_organization():

    class FilteredFakeRetriever(FakeRetriever):

        def filter_results(
            self,
            results,
            source_organization=None,
            module=None,
            document_name=None,
        ):
            if source_organization == "CFC":
                return results

            return []

    rag = RAG(
        retriever=FilteredFakeRetriever()
    )

    results = rag.retrieve(
        "Reforma Tributária",
        source_organization="CFC",
    )

    assert len(results) == 1


# ============================================================
# TESTE 18 — FILTRO POR MÓDULO
# ============================================================

def test_retrieve_with_module():

    class FilteredFakeRetriever(FakeRetriever):

        def filter_results(
            self,
            results,
            source_organization=None,
            module=None,
            document_name=None,
        ):
            if module == "Modulo 1":
                return results

            return []

    rag = RAG(
        retriever=FilteredFakeRetriever()
    )

    results = rag.retrieve(
        "Reforma Tributária",
        module="Modulo 1",
    )

    assert len(results) == 1


# ============================================================
# TESTE 19 — FILTRO POR DOCUMENTO
# ============================================================

def test_retrieve_with_document():

    class FilteredFakeRetriever(FakeRetriever):

        def filter_results(
            self,
            results,
            source_organization=None,
            module=None,
            document_name=None,
        ):
            if document_name == "Modulo_1_parte_1.pdf":
                return results

            return []

    rag = RAG(
        retriever=FilteredFakeRetriever()
    )

    results = rag.retrieve(
        "Reforma Tributária",
        document_name="Modulo_1_parte_1.pdf",
    )

    assert len(results) == 1


# ============================================================
# TESTE 20 — COMBINAÇÃO DE FILTROS
# ============================================================

def test_retrieve_with_combined_filters():

    class FilteredFakeRetriever(FakeRetriever):

        def filter_results(
            self,
            results,
            source_organization=None,
            module=None,
            document_name=None,
        ):
            if (
                source_organization == "CFC"
                and module == "Modulo 1"
                and document_name == "Modulo_1_parte_1.pdf"
            ):
                return results

            return []

    rag = RAG(
        retriever=FilteredFakeRetriever()
    )

    results = rag.retrieve(
        "Reforma Tributária",
        source_organization="CFC",
        module="Modulo 1",
        document_name="Modulo_1_parte_1.pdf",
    )

    assert len(results) == 1
