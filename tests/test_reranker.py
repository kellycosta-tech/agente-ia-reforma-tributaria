"""
Testes do módulo de reranking.

Valida:

    - carregamento do modelo;
    - validação dos parâmetros;
    - reranking dos resultados;
    - preservação dos metadados;
    - ordenação por score;
    - quantidade de resultados retornados.
"""

from unittest.mock import MagicMock

import pytest

from vectorstore.reranker import (
    load_reranker_model,
    rerank_results,
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def fake_model():
    """
    Modelo CrossEncoder simulado para evitar
    download e processamento real durante os testes.
    """

    model = MagicMock()

    model.predict.return_value = [
        0.2,
        0.9,
        0.5,
    ]

    return model


@pytest.fixture
def sample_results():
    """
    Resultados simulados do Retriever.
    """

    return [
        {
            "chunk_id": "chunk_001",
            "document_id": "doc_001",
            "document_name": "Modulo_1_parte_1.pdf",
            "source_organization": "CFC",
            "page": 9,
            "text": "Princípios constitucionais da Reforma Tributária.",
        },
        {
            "chunk_id": "chunk_002",
            "document_id": "doc_002",
            "document_name": "Modulo_2_parte_1.pdf",
            "source_organization": "CFC",
            "page": 12,
            "text": "Tributação sobre bens e serviços.",
        },
        {
            "chunk_id": "chunk_003",
            "document_id": "doc_003",
            "document_name": "Modulo_3_parte_1.pdf",
            "source_organization": "Receita Federal",
            "page": 20,
            "text": "Regras da Reforma Tributária.",
        },
    ]


# ============================================================
# LOAD MODEL
# ============================================================

def test_load_reranker_model(monkeypatch):
    """
    Verifica se o carregamento do modelo funciona.
    """

    mock_cross_encoder = MagicMock()

    monkeypatch.setattr(
        "vectorstore.reranker.CrossEncoder",
        mock_cross_encoder,
    )

    load_reranker_model()

    mock_cross_encoder.assert_called_once()


# ============================================================
# QUERY
# ============================================================

def test_rerank_query_must_be_string(
    fake_model,
    sample_results,
):
    """
    Query deve ser uma string.
    """

    with pytest.raises(TypeError):
        rerank_results(
            query=123,
            results=sample_results,
            model=fake_model,
            k=3,
        )


def test_rerank_query_cannot_be_empty(
    fake_model,
    sample_results,
):
    """
    Query vazia deve gerar erro.
    """

    with pytest.raises(ValueError):
        rerank_results(
            query="   ",
            results=sample_results,
            model=fake_model,
            k=3,
        )


# ============================================================
# RESULTS
# ============================================================

def test_rerank_results_must_be_list(
    fake_model,
):
    """
    results deve ser uma lista.
    """

    with pytest.raises(TypeError):
        rerank_results(
            query="Reforma Tributária",
            results="invalid",
            model=fake_model,
            k=3,
        )


def test_rerank_results_preserves_metadata(
    fake_model,
    sample_results,
):
    """
    O reranker deve preservar os metadados originais.
    """

    results = rerank_results(
        query="Reforma Tributária",
        results=sample_results,
        model=fake_model,
        k=3,
    )

    assert len(results) == 3

    for result in results:
        assert "chunk_id" in result
        assert "document_id" in result
        assert "document_name" in result
        assert "source_organization" in result
        assert "page" in result
        assert "text" in result


# ============================================================
# SCORE
# ============================================================

def test_rerank_adds_score(
    fake_model,
    sample_results,
):
    """
    Cada resultado deve receber o campo rerank_score.
    """

    results = rerank_results(
        query="Reforma Tributária",
        results=sample_results,
        model=fake_model,
        k=3,
    )

    for result in results:
        assert "rerank_score" in result
        assert isinstance(
            result["rerank_score"],
            float,
        )


# ============================================================
# ORDER
# ============================================================

def test_rerank_orders_by_score(
    fake_model,
    sample_results,
):
    """
    Resultados devem ser ordenados pelo score
    do maior para o menor.
    """

    results = rerank_results(
        query="Reforma Tributária",
        results=sample_results,
        model=fake_model,
        k=3,
    )

    scores = [
        result["rerank_score"]
        for result in results
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )


# ============================================================
# TOP-K
# ============================================================

def test_rerank_respects_k(
    fake_model,
    sample_results,
):
    """
    O reranker deve retornar somente os K
    resultados solicitados.
    """

    results = rerank_results(
        query="Reforma Tributária",
        results=sample_results,
        model=fake_model,
        k=2,
    )

    assert len(results) == 2


def test_rerank_k_must_be_positive(
    fake_model,
    sample_results,
):
    """
    k deve ser maior que zero.
    """

    with pytest.raises(ValueError):
        rerank_results(
            query="Reforma Tributária",
            results=sample_results,
            model=fake_model,
            k=0,
        )


# ============================================================
# EMPTY RESULTS
# ============================================================

def test_rerank_empty_results(
    fake_model,
):
    """
    Lista vazia deve retornar lista vazia.
    """

    results = rerank_results(
        query="Reforma Tributária",
        results=[],
        model=fake_model,
        k=5,
    )

    assert results == []
