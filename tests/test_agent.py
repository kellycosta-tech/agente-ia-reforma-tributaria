"""
Testes da camada Agent.

Valida a integração entre:

    Agent
      ↓
    RAG
      ↓
    Retriever
      ↓
    Vector Store

Nesta etapa, o LLM ainda não é utilizado.
"""

import pytest

from app.agent import (
    Agent,
    create_agent,
    prepare_llm_input,
)


# ============================================================
# MOCK RAG
# ============================================================

class FakeRAG:
    """
    RAG simplificado para testes unitários.
    """

    def retrieve_context(
        self,
        query: str,
        k: int = 5,
        source_organization=None,
        module=None,
        document_name=None,
    ):
        return {
            "query": query,
            "results": [
                {
                    "chunk_id": "chunk_0001",
                    "document_id": "doc_001",
                    "document_name": "Modulo_1_parte_1.pdf",
                    "source_organization": "CFC",
                    "page": 10,
                    "module": "Modulo 1",
                    "text": (
                        "A Reforma Tributária altera "
                        "a tributação sobre o consumo."
                    ),
                    "similarity": 0.95,
                }
            ][:k],
            "context": (
                "[Fonte 1]\n"
                "Documento: Modulo_1_parte_1.pdf\n"
                "Organização: CFC\n"
                "Página: 10\n"
                "Conteúdo: A Reforma Tributária "
                "altera a tributação sobre o consumo."
            ),
        }


# ============================================================
# TESTE 1
# ============================================================

def test_create_agent():

    agent = Agent(
        rag=FakeRAG()
    )

    assert agent is not None


# ============================================================
# TESTE 2
# ============================================================

def test_create_agent_invalid_rag():

    with pytest.raises(TypeError):

        Agent(
            rag=object()
        )


# ============================================================
# TESTE 3
# ============================================================

def test_query():

    agent = Agent(
        rag=FakeRAG()
    )

    result = agent.query(
        "O que é a Reforma Tributária?"
    )

    assert isinstance(
        result,
        dict,
    )

    assert "query" in result

    assert "results" in result

    assert "context" in result


# ============================================================
# TESTE 4
# ============================================================

def test_query_preserves_question():

    agent = Agent(
        rag=FakeRAG()
    )

    result = agent.query(
        "O que é a Reforma Tributária?"
    )

    assert result["query"] == (
        "O que é a Reforma Tributária?"
    )


# ============================================================
# TESTE 5
# ============================================================

def test_query_preserves_results():

    agent = Agent(
        rag=FakeRAG()
    )

    result = agent.query(
        "O que é a Reforma Tributária?"
    )

    assert len(
        result["results"]
    ) == 1

    assert (
        result["results"][0]["chunk_id"]
        == "chunk_0001"
    )


# ============================================================
# TESTE 6
# ============================================================

def test_query_preserves_sources():

    agent = Agent(
        rag=FakeRAG()
    )

    result = agent.query(
        "O que é a Reforma Tributária?"
    )

    source = result["results"][0]

    assert (
        source["document_name"]
        == "Modulo_1_parte_1.pdf"
    )

    assert (
        source["source_organization"]
        == "CFC"
    )

    assert source["page"] == 10


# ============================================================
# TESTE 7
# ============================================================

def test_query_empty_question():

    agent = Agent(
        rag=FakeRAG()
    )

    with pytest.raises(ValueError):

        agent.query("")


# ============================================================
# TESTE 8
# ============================================================

def test_query_whitespace_question():

    agent = Agent(
        rag=FakeRAG()
    )

    with pytest.raises(ValueError):

        agent.query("   ")


# ============================================================
# TESTE 9
# ============================================================

def test_query_invalid_question():

    agent = Agent(
        rag=FakeRAG()
    )

    with pytest.raises(TypeError):

        agent.query(123)


# ============================================================
# TESTE 10
# ============================================================

def test_query_invalid_k():

    agent = Agent(
        rag=FakeRAG()
    )

    with pytest.raises(ValueError):

        agent.query(
            "Reforma Tributária",
            k=0,
        )


# ============================================================
# TESTE 11
# ============================================================

def test_query_invalid_k_type():

    agent = Agent(
        rag=FakeRAG()
    )

    with pytest.raises(TypeError):

        agent.query(
            "Reforma Tributária",
            k="5",
        )


# ============================================================
# TESTE 12
# ============================================================

def test_query_with_source_organization():

    agent = Agent(
        rag=FakeRAG()
    )

    result = agent.query(
        "Reforma Tributária",
        source_organization="CFC",
    )

    assert result is not None

    assert result["results"][0][
        "source_organization"
    ] == "CFC"


# ============================================================
# TESTE 13
# ============================================================

def test_query_with_module():

    agent = Agent(
        rag=FakeRAG()
    )

    result = agent.query(
        "Reforma Tributária",
        module="Modulo 1",
    )

    assert result is not None


# ============================================================
# TESTE 14
# ============================================================

def test_query_with_document():

    agent = Agent(
        rag=FakeRAG()
    )

    result = agent.query(
        "Reforma Tributária",
        document_name="Modulo_1_parte_1.pdf",
    )

    assert result is not None


# ============================================================
# TESTE 15
# ============================================================

def test_query_with_combined_filters():

    agent = Agent(
        rag=FakeRAG()
    )

    result = agent.query(
        "Reforma Tributária",
        source_organization="CFC",
        module="Modulo 1",
        document_name="Modulo_1_parte_1.pdf",
    )

    assert result is not None


# ============================================================
# TESTE 16
# ============================================================

def test_prepare_llm_input():

    context_result = {
        "query": "O que é a Reforma Tributária?",
        "results": [
            {
                "chunk_id": "chunk_0001",
                "document_name": "Modulo_1_parte_1.pdf",
                "source_organization": "CFC",
                "page": 10,
                "text": "Conteúdo sobre Reforma Tributária.",
            }
        ],
        "context": (
            "Conteúdo sobre Reforma Tributária."
        ),
    }

    result = prepare_llm_input(
        question="O que é a Reforma Tributária?",
        context_result=context_result,
    )

    assert isinstance(
        result,
        dict,
    )

    assert (
        result["question"]
        == "O que é a Reforma Tributária?"
    )

    assert "context" in result

    assert "sources" in result


# ============================================================
# TESTE 17
# ============================================================

def test_prepare_llm_input_preserves_context():

    context_result = {
        "query": "Pergunta",
        "results": [],
        "context": "Contexto recuperado.",
    }

    result = prepare_llm_input(
        question="Pergunta",
        context_result=context_result,
    )

    assert (
        result["context"]
        == "Contexto recuperado."
    )


# ============================================================
# TESTE 18
# ============================================================

def test_prepare_llm_input_preserves_sources():

    sources = [
        {
            "chunk_id": "chunk_0001",
            "document_name": "documento.pdf",
            "page": 15,
        }
    ]

    context_result = {
        "query": "Pergunta",
        "results": sources,
        "context": "Contexto.",
    }

    result = prepare_llm_input(
        question="Pergunta",
        context_result=context_result,
    )

    assert result["sources"] == sources


# ============================================================
# TESTE 19
# ============================================================

def test_prepare_llm_input_invalid_question():

    with pytest.raises(TypeError):

        prepare_llm_input(
            question=123,
            context_result={
                "context": "Contexto.",
                "results": [],
            },
        )


# ============================================================
# TESTE 20
# ============================================================

def test_prepare_llm_input_empty_question():

    with pytest.raises(ValueError):

        prepare_llm_input(
            question="",
            context_result={
                "context": "Contexto.",
                "results": [],
            },
        )


# ============================================================
# TESTE 21
# ============================================================

def test_prepare_llm_input_invalid_context():

    with pytest.raises(TypeError):

        prepare_llm_input(
            question="Pergunta",
            context_result=None,
        )


# ============================================================
# TESTE 22
# ============================================================

def test_prepare_llm_input_missing_context():

    with pytest.raises(ValueError):

        prepare_llm_input(
            question="Pergunta",
            context_result={
                "results": [],
            },
        )


# ============================================================
# TESTE 23
# ============================================================

def test_prepare_llm_input_missing_results():

    with pytest.raises(ValueError):

        prepare_llm_input(
            question="Pergunta",
            context_result={
                "context": "Contexto.",
            },
        )


# ============================================================
# TESTE 24
# ============================================================

def test_create_agent_with_fake_rag():

    agent = create_agent(
        rag=FakeRAG()
    )

    assert isinstance(
        agent,
        Agent,
    )

    assert agent.rag is not None