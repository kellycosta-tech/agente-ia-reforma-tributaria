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
      ↓
    Contexto
      ↓
    Prompt
      ↓
    LLM

O LLM utilizado nos testes é uma implementação
controlada/falsa, sem chamadas externas.
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
# FAKE LLM PARA TESTE DE INTEGRAÇÃO
# ============================================================

class RecordingLLM:
    """
    LLM falso utilizado para verificar a integração
    entre Agent → Prompt → LLM.
    """

    def __init__(
        self,
        response: str = "Resposta baseada no contexto.",
    ):
        self.response = response
        self.received_prompt = None

    def generate(
        self,
        prompt: str,
    ) -> str:

        if not isinstance(prompt, str):
            raise TypeError(
                "prompt deve ser uma string."
            )

        self.received_prompt = prompt

        return self.response
# ============================================================
# TESTE 1
# ============================================================

def test_create_agent():

    agent = Agent(
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
)

    with pytest.raises(ValueError):

        agent.query("")


# ============================================================
# TESTE 8
# ============================================================

def test_query_whitespace_question():

    agent = Agent(
    rag=FakeRAG(),
    llm=RecordingLLM(),
)

    with pytest.raises(ValueError):

        agent.query("   ")


# ============================================================
# TESTE 9
# ============================================================

def test_query_invalid_question():

    agent = Agent(
    rag=FakeRAG(),
    llm=RecordingLLM(),
)

    with pytest.raises(TypeError):

        agent.query(123)


# ============================================================
# TESTE 10
# ============================================================

def test_query_invalid_k():

    agent = Agent(
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
    rag=FakeRAG(),
    llm=RecordingLLM(),
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
# ============================================================
# TESTE 25
# ============================================================

def test_agent_calls_llm():

    llm = RecordingLLM(
        response="A Reforma Tributária altera a tributação."
    )

    agent = Agent(
        rag=FakeRAG(),
        llm=llm,
    )

    result = agent.ask(
        "O que é a Reforma Tributária?"
    )

    assert result["answer"] == (
        "A Reforma Tributária altera a tributação."
    )

    assert llm.received_prompt is not None
# ============================================================
# TESTE 26
# ============================================================

def test_agent_prompt_contains_question():

    llm = RecordingLLM()

    agent = Agent(
        rag=FakeRAG(),
        llm=llm,
    )

    agent.ask(
        "O que é o IBS?"
    )

    assert "O que é o IBS?" in (
        llm.received_prompt
    )
# ============================================================
# TESTE 27
# ============================================================

def test_agent_prompt_contains_context():

    llm = RecordingLLM()

    agent = Agent(
        rag=FakeRAG(),
        llm=llm,
    )

    agent.ask(
        "O que é a Reforma Tributária?"
    )

    assert (
        "A Reforma Tributária altera"
        in llm.received_prompt
    )
# ============================================================
# TESTE 28
# ============================================================

def test_agent_prompt_contains_system_instructions():

    llm = RecordingLLM()

    agent = Agent(
        rag=FakeRAG(),
        llm=llm,
    )

    agent.ask(
        "O que é a Reforma Tributária?"
    )

    assert (
        "Utilize somente informações presentes no contexto"
        in llm.received_prompt
    )
# ============================================================
# FAKE RAG SEM CONTEXTO
# ============================================================

class EmptyRAG:

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
            "results": [],
            "context": "",
        }
# ============================================================
# TESTE 29
# ============================================================

def test_agent_fallback_without_context():

    llm = RecordingLLM()

    agent = Agent(
        rag=EmptyRAG(),
        llm=llm,
    )

    result = agent.ask(
        "Pergunta sem evidência documental."
    )

    assert (
        "Não encontrei evidências suficientes"
        in result["answer"]
    )

    assert result["sources"] == []

    assert result["context"] == ""

    assert llm.received_prompt is None

# ============================================================
# TESTE 30
# ============================================================

def test_agent_returns_sources():

    llm = RecordingLLM()

    agent = Agent(
        rag=FakeRAG(),
        llm=llm,
    )

    result = agent.ask(
        "O que é a Reforma Tributária?"
    )

    assert len(result["sources"]) == 1

    source = result["sources"][0]

    assert source["document_name"] == (
        "Modulo_1_parte_1.pdf"
    )

    assert source["page"] == 10

    assert source["source_organization"] == "CFC"

# ============================================================
# TESTE 31
# ============================================================

def test_agent_returns_answer_as_string():

    llm = RecordingLLM(
        response="Resposta fundamentada."
    )

    agent = Agent(
        rag=FakeRAG(),
        llm=llm,
    )

    result = agent.ask(
        "O que é a Reforma Tributária?"
    )

    assert isinstance(
        result["answer"],
        str,
    )

    assert result["answer"] == (
        "Resposta fundamentada."
    )


# ============================================================
# TESTE 32
# ============================================================

def test_agent_preserves_context():

    llm = RecordingLLM()

    agent = Agent(
        rag=FakeRAG(),
        llm=llm,
    )

    result = agent.ask(
        "O que é a Reforma Tributária?"
    )

    assert (
        "A Reforma Tributária altera"
        in result["context"]
    )


# ============================================================
# TESTE 33
# ============================================================

def test_agent_returns_formatted_sources():

    llm = RecordingLLM()

    agent = Agent(
        rag=FakeRAG(),
        llm=llm,
    )

    result = agent.ask(
        "O que é a Reforma Tributária?"
    )

    assert result["sources"] == [
        {
            "document_name": "Modulo_1_parte_1.pdf",
            "page": 10,
            "section": None,
            "source_organization": "CFC",
        }
    ]


# ============================================================
# TESTE 34
# ============================================================

def test_agent_does_not_call_llm_without_context():

    llm = RecordingLLM()

    agent = Agent(
        rag=EmptyRAG(),
        llm=llm,
    )

    result = agent.ask(
        "Qual é a alíquota do IBS?"
    )

    assert llm.received_prompt is None

    assert result["answer"].startswith(
        "Não encontrei evidências suficientes"
    )