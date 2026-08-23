"""
Testes da avaliação da recuperação do RAG.
"""

import pytest

from evaluation.evaluate_retrieval import (
    evaluate_question,
    evaluate_retrieval,
    normalize_text,
)


# ============================================================
# FAKE RAG
# ============================================================

class FakeRAG:

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ):

        results = [
            {
                "chunk_id": "chunk_001",
                "document_name": "Modulo_1_parte_1.pdf",
                "source_organization": "CFC",
                "page": 1,
                "text": "Conteúdo da Reforma Tributária.",
                "similarity": 0.95,
            },
            {
                "chunk_id": "chunk_002",
                "document_name": "Modulo_2.pdf",
                "source_organization": "CFC",
                "page": 20,
                "text": "Outro conteúdo.",
                "similarity": 0.80,
            },
        ]

        return results[:k]


# ============================================================
# NORMALIZAÇÃO
# ============================================================

def test_normalize_text():

    assert normalize_text(
        "  CFC  "
    ) == "cfc"


# ============================================================
# AVALIAÇÃO DE HIT
# ============================================================

def test_evaluate_question_hit():

    question = {
        "id": "q001",
        "question": "O que é a Reforma Tributária?",
        "expected_document": (
            "Modulo_1_parte_1.pdf"
        ),
        "expected_source": "CFC",
        "expected_pages": [1],
    }

    result = evaluate_question(
        rag=FakeRAG(),
        question=question,
        k=5,
    )

    assert result["document_hit"] is True

    assert result["source_hit"] is True

    assert result["page_hit"] is True

    assert result["hit_at_k"] is True

    assert result["document_rank"] == 1

    assert result["reciprocal_rank"] == 1.0


# ============================================================
# DOCUMENTO NÃO ENCONTRADO
# ============================================================

def test_evaluate_question_document_miss():

    question = {
        "id": "q002",
        "question": "Pergunta",
        "expected_document": "Outro_documento.pdf",
        "expected_source": "CFC",
        "expected_pages": [10],
    }

    result = evaluate_question(
        rag=FakeRAG(),
        question=question,
        k=5,
    )

    assert result["document_hit"] is False

    assert result["hit_at_k"] is False

    assert result["document_rank"] is None

    assert result["reciprocal_rank"] == 0.0


# ============================================================
# PÁGINA INCORRETA
# ============================================================

def test_evaluate_question_wrong_page():

    question = {
        "id": "q003",
        "question": "Pergunta",
        "expected_document": (
            "Modulo_1_parte_1.pdf"
        ),
        "expected_source": "CFC",
        "expected_pages": [99],
    }

    result = evaluate_question(
        rag=FakeRAG(),
        question=question,
        k=5,
    )

    assert result["document_hit"] is True

    assert result["source_hit"] is True

    assert result["page_hit"] is False

    assert result["hit_at_k"] is False


# ============================================================
# RANK 2
# ============================================================

def test_evaluate_question_rank_two():

    class RankTwoRAG:

        def retrieve(
            self,
            query,
            k=5,
        ):

            return [
                {
                    "document_name": "Outro.pdf",
                    "source_organization": "CFC",
                    "page": 20,
                },
                {
                    "document_name": "Esperado.pdf",
                    "source_organization": "CFC",
                    "page": 10,
                },
            ][:k]

    question = {
        "id": "q004",
        "question": "Pergunta",
        "expected_document": "Esperado.pdf",
        "expected_source": "CFC",
        "expected_pages": [10],
    }

    result = evaluate_question(
        rag=RankTwoRAG(),
        question=question,
        k=5,
    )

    assert result["hit_at_k"] is True

    assert result["document_rank"] == 2

    assert result["page_rank"] == 2

    assert result["reciprocal_rank"] == 0.5


# ============================================================
# AVALIAÇÃO COMPLETA
# ============================================================

def test_evaluate_retrieval():

    questions = [
        {
            "id": "q001",
            "question": "Pergunta 1",
            "expected_document": (
                "Modulo_1_parte_1.pdf"
            ),
            "expected_source": "CFC",
            "expected_pages": [1],
        },
        {
            "id": "q002",
            "question": "Pergunta 2",
            "expected_document": (
                "Documento_inexistente.pdf"
            ),
            "expected_source": "CFC",
            "expected_pages": [1],
        },
    ]

    result = evaluate_retrieval(
        rag=FakeRAG(),
        questions=questions,
        k=5,
    )

    assert result["total_questions"] == 2

    assert result["k"] == 5

    assert result["hit_at_k"] == 0.5

    assert result["document_hit_rate"] == 0.5

    assert result["source_hit_rate"] == 1.0

    assert result["page_hit_rate"] == 0.5

    assert result["mrr"] == 0.5


# ============================================================
# VALIDAÇÕES
# ============================================================

def test_evaluate_question_invalid_question():

    with pytest.raises(TypeError):

        evaluate_question(
            rag=FakeRAG(),
            question=None,
        )


def test_evaluate_question_empty_question():

    with pytest.raises(ValueError):

        evaluate_question(
            rag=FakeRAG(),
            question={
                "question": "",
                "expected_document": "doc.pdf",
                "expected_source": "CFC",
                "expected_pages": [1],
            },
        )


def test_evaluate_retrieval_empty_questions():

    with pytest.raises(ValueError):

        evaluate_retrieval(
            rag=FakeRAG(),
            questions=[],
        )


def test_evaluate_retrieval_invalid_questions():

    with pytest.raises(TypeError):

        evaluate_retrieval(
            rag=FakeRAG(),
            questions=None,
        )