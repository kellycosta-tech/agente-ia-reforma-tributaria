"""
Agente de IA para consulta à base documental.

Responsabilidades:

    1. Receber a pergunta do usuário.
    2. Acionar a camada RAG.
    3. Recuperar os chunks relevantes.
    4. Montar o contexto.
    5. Preparar a entrada para o LLM.
    6. Construir o prompt.
    7. Enviar o prompt ao LLM.
    8. Retornar a resposta juntamente com as fontes.

Fluxo:

    Pergunta
       ↓
    Agent
       ↓
    RAG
       ↓
    Retriever
       ↓
    Contexto
       ↓
    Prompt
       ↓
    LLM
       ↓
    Resposta + Fontes
"""

from __future__ import annotations

from typing import Any

from llm import (
    BaseLLM,
    create_llm,
)

from prompts import (
    build_messages,
)

from rag import (
    RAG,
    create_rag,
)


# ============================================================
# PREPARAÇÃO DA ENTRADA DO LLM
# ============================================================

def prepare_llm_input(
    question: str,
    context_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Prepara os dados recuperados pelo RAG para utilização pelo LLM.

    Parameters
    ----------
    question:
        Pergunta original do usuário.

    context_result:
        Resultado produzido pelo RAG.retrieve_context().

    Returns
    -------
    dict[str, Any]
        Estrutura contendo pergunta, contexto e fontes.
    """

    # --------------------------------------------------------
    # Validação da pergunta
    # --------------------------------------------------------

    if not isinstance(question, str):
        raise TypeError(
            "question deve ser uma string."
        )

    question = question.strip()

    if not question:
        raise ValueError(
            "question não pode estar vazia."
        )

    # --------------------------------------------------------
    # Validação do contexto
    # --------------------------------------------------------

    if not isinstance(context_result, dict):
        raise TypeError(
            "context_result deve ser um dicionário."
        )

    if "context" not in context_result:
        raise ValueError(
            "context_result deve conter o campo 'context'."
        )

    if "results" not in context_result:
        raise ValueError(
            "context_result deve conter o campo 'results'."
        )

    context = context_result["context"]
    results = context_result["results"]

    if not isinstance(context, str):
        raise TypeError(
            "context deve ser uma string."
        )

    if not isinstance(results, list):
        raise TypeError(
            "results deve ser uma lista."
        )

    if not context.strip():
        raise ValueError(
            "context não pode estar vazio."
        )

    return {
        "question": question,
        "context": context,
        "sources": results,
    }


# ============================================================
# AGENT
# ============================================================

class Agent:
    """
    Orquestra o fluxo completo de consulta do agente.

    Fluxo:

        Pergunta
           ↓
        RAG
           ↓
        Contexto
           ↓
        Prompt
           ↓
        LLM
           ↓
        Resposta
    """

    def __init__(
        self,
        rag: RAG | None = None,
        llm: BaseLLM | None = None,
    ) -> None:

        if rag is None:
            rag = create_rag()

        if llm is None:
            llm = create_llm()

        if not hasattr(rag, "retrieve_context"):
            raise TypeError(
                "rag deve possuir o método "
                "'retrieve_context'."
            )

        if not hasattr(llm, "generate"):
            raise TypeError(
                "llm deve possuir o método "
                "'generate'."
            )

        self.rag = rag
        self.llm = llm

    # ========================================================
    # QUERY
    # ========================================================

    def query(
        self,
        query: str,
        k: int = 5,
        source_organization: str | None = None,
        module: str | None = None,
        document_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Alias de compatibilidade para ask().

        Mantém uma interface simples para consultas.
        """

        return self.ask(
            query=query,
            k=k,
            source_organization=source_organization,
            module=module,
            document_name=document_name,
        )

    # ========================================================
    # ASK
    # ========================================================

    def ask(
        self,
        query: str,
        k: int = 5,
        source_organization: str | None = None,
        module: str | None = None,
        document_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Executa uma consulta completa no agente.

        Fluxo:

            Pergunta
                ↓
            RAG
                ↓
            Contexto
                ↓
            Prompt
                ↓
            LLM
                ↓
            Resposta + Fontes
        """

        # ----------------------------------------------------
        # 1. Validação da pergunta
        # ----------------------------------------------------

        if not isinstance(query, str):
            raise TypeError(
                "query deve ser uma string."
            )

        query = query.strip()

        if not query:
            raise ValueError(
                "query não pode estar vazia."
            )

        # ----------------------------------------------------
        # 2. Validação de k
        # ----------------------------------------------------

        if not isinstance(k, int):
            raise TypeError(
                "k deve ser um inteiro."
            )

        if k <= 0:
            raise ValueError(
                "k deve ser maior que zero."
            )

        # ----------------------------------------------------
        # 3. RAG
        # ----------------------------------------------------

        rag_result = self.rag.retrieve_context(
            query=query,
            k=k,
            source_organization=source_organization,
            module=module,
            document_name=document_name,
        )

        if not isinstance(rag_result, dict):
            raise TypeError(
                "RAG deve retornar um dicionário."
            )

        # ----------------------------------------------------
        # 4. Preparação dos dados
        # ----------------------------------------------------

        context = rag_result.get(
            "context",
            "",
        )

        results = rag_result.get(
            "results",
            [],
        )

        # ----------------------------------------------------
        # 5. Fallback
        # ----------------------------------------------------

        if not context or not str(context).strip():

            return {
                "query": query,
                "answer": (
                    "Não encontrei evidências suficientes "
                    "nos documentos disponíveis para "
                    "responder a essa pergunta com segurança."
                ),
                "context": "",
                "sources": [],
                "results": results,
            }

        # ----------------------------------------------------
        # 6. Preparar entrada do LLM
        # ----------------------------------------------------

        llm_input = prepare_llm_input(
            question=query,
            context_result=rag_result,
        )

        # ----------------------------------------------------
        # 7. Construir mensagens
        # ----------------------------------------------------

        messages = build_messages(
            query=llm_input["question"],
            context=llm_input["context"],
        )

        # ----------------------------------------------------
        # 8. Converter mensagens em prompt
        # ----------------------------------------------------

        system_message = messages[0]["content"]
        user_message = messages[1]["content"]

        prompt = (
            f"{system_message}\n\n"
            f"{user_message}"
        )

        # ----------------------------------------------------
        # 9. Enviar para o LLM
        # ----------------------------------------------------

        answer = self.llm.generate(
            prompt,
        )

        if not isinstance(answer, str):
            raise TypeError(
                "O LLM deve retornar uma string."
            )

        answer = answer.strip()

        if not answer:
            raise ValueError(
                "O LLM retornou uma resposta vazia."
            )

        # ----------------------------------------------------
        # 10. Extrair fontes
        # ----------------------------------------------------

        sources = self._extract_sources(
            results,
        )

        # ----------------------------------------------------
        # 11. Resultado final
        # ----------------------------------------------------

        return {
            "query": query,
            "answer": answer,
            "context": context,
            "sources": sources,
            "results": results,
        }

    # ========================================================
    # SOURCES
    # ========================================================

    @staticmethod
    def _extract_sources(
        results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Extrai informações de rastreabilidade
        dos chunks recuperados.
        """

        if not isinstance(results, list):
            raise TypeError(
                "results deve ser uma lista."
            )

        sources: list[dict[str, Any]] = []

        seen: set[tuple[Any, ...]] = set()

        for result in results:

            if not isinstance(result, dict):
                continue

            document_name = result.get(
                "document_name"
            )

            page = result.get(
                "page"
            )

            source_organization = result.get(
                "source_organization"
            )

            section = result.get(
                "section"
            )

            source_key = (
                document_name,
                page,
                section,
            )

            if source_key in seen:
                continue

            seen.add(source_key)

            sources.append(
                {
                    "document_name": document_name,
                    "page": page,
                    "section": section,
                    "source_organization": (
                        source_organization
                    ),
                }
            )

        return sources


# ============================================================
# FACTORY
# ============================================================

def create_agent(
    rag: RAG | None = None,
    llm: BaseLLM | None = None,
) -> Agent:
    """
    Cria uma instância configurada do Agent.
    """

    return Agent(
        rag=rag,
        llm=llm,
    )