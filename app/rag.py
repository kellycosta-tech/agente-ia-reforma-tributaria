"""
Camada de recuperação e montagem de contexto do RAG.

Responsabilidades:

    1. Receber uma pergunta do usuário.
    2. Utilizar o Retriever para realizar a busca semântica.
    3. Recuperar os chunks mais relevantes.
    4. Preservar os metadados dos documentos.
    5. Aplicar filtros por metadados.
    6. Montar um contexto estruturado para o LLM.

Fluxo:

    Pergunta
       ↓
    RAG
       ↓
    Retriever
       ↓
    Query Embedding
       ↓
    Vector Store
       ↓
    Chunks relevantes
       ↓
    Filtros
       ↓
    Context Builder
       ↓
    Contexto estruturado
       ↓
    LLM
"""

from __future__ import annotations

from typing import Any

from vectorstore.retriever import create_retriever


# ============================================================
# RAG
# ============================================================

class RAG:
    """
    Orquestra a camada de recuperação do pipeline RAG.

    Responsabilidades:

        - executar a recuperação semântica;
        - aplicar filtros por metadados;
        - preservar os metadados;
        - montar o contexto estruturado.
    """

    def __init__(
        self,
        retriever: Any,
    ) -> None:
        """
        Inicializa o RAG.

        Parameters
        ----------
        retriever:
            Objeto responsável pela recuperação semântica.
            Deve possuir o método ``retrieve``.
        """

        if not hasattr(retriever, "retrieve"):
            raise TypeError(
                "retriever deve possuir o método 'retrieve'."
            )

        self.retriever = retriever

    # ========================================================
    # RECUPERAÇÃO
    # ========================================================

    def retrieve(
        self,
        query: str,
        k: int = 5,
        source_organization: str | None = None,
        module: str | None = None,
        document_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Recupera os chunks mais relevantes para uma pergunta.

        Os filtros são opcionais e permitem restringir a recuperação
        por organização, módulo ou documento.
        """

        if not isinstance(query, str):
            raise TypeError(
                "query deve ser uma string."
            )

        query = query.strip()

        if not query:
            raise ValueError(
                "query não pode estar vazia."
            )

        if not isinstance(k, int):
            raise TypeError(
                "k deve ser um inteiro."
            )

        if k <= 0:
            raise ValueError(
                "k deve ser maior que zero."
            )

# ========================================================
# RECUPERAÇÃO SEMÂNTICA
# ========================================================

        results = self.retriever.retrieve(
            query=query,
            k=k,
        )

# ========================================================
# FILTROS POR METADADOS
# ========================================================

        if hasattr(self.retriever, "filter_results"):
            results = self.retriever.filter_results(
                results=results,
                source_organization=source_organization,
                module=module,
                document_name=document_name,
            )

        return results

 # ========================================================
    # MONTAGEM DO CONTEXTO
 # ========================================================

    def build_context(
        self,
        results: list[dict[str, Any]],
    ) -> str:
        """
        Monta um contexto estruturado a partir dos chunks recuperados.

        O contexto mantém as informações necessárias para rastreabilidade
        da resposta, incluindo documento, instituição, página, seção
        e conteúdo.
        """

        if not isinstance(results, list):
            raise TypeError(
                "results deve ser uma lista."
            )

        if not results:
            return ""

        context_parts: list[str] = []

        for index, result in enumerate(results, start=1):

            if not isinstance(result, dict):
                raise TypeError(
                    "Cada resultado deve ser um dicionário."
                )

            document_name = result.get(
                "document_name",
                "Documento não informado",
            )

            source_organization = result.get(
                "source_organization",
                "Organização não informada",
            )

            page = result.get(
                "page",
                "Página não informada",
            )

            section = result.get(
                "section",
                None,
            )

            text = result.get(
                "text",
                "",
            )

            if not isinstance(text, str):
                raise TypeError(
                    "O campo 'text' deve ser uma string."
                )

            text = text.strip()

            if not text:
                continue

            source_block = (
                f"[Fonte {index}]\n"
                f"Documento: {document_name}\n"
                f"Instituição: {source_organization}\n"
                f"Página: {page}\n"
            )

            if section:
                source_block += (
                    f"Seção: {section}\n"
                )

            source_block += (
                "\n"
                "Conteúdo:\n"
                f"{text}"
            )

            context_parts.append(
                source_block
            )

        return "\n\n".join(
            context_parts
        )

    # ========================================================
    # RECUPERAÇÃO + CONTEXTO
    # ========================================================

    def retrieve_context(
        self,
        query: str,
        k: int = 5,
        source_organization: str | None = None,
        module: str | None = None,
        document_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Executa a recuperação e monta o contexto estruturado.

        Retorna:

            {
                "query": pergunta,
                "results": chunks recuperados,
                "context": contexto estruturado
            }
        """

        results = self.retrieve(
            query=query,
            k=k,
            source_organization=source_organization,
            module=module,
            document_name=document_name,
        )

        context = self.build_context(
            results
        )

        return {
            "query": query,
            "results": results,
            "context": context,
        }


# ============================================================
# FACTORY
# ============================================================

def create_rag(
    retriever: Any | None = None,
) -> RAG:
    """
    Cria uma instância configurada da camada RAG.

    Se nenhum Retriever for fornecido, um Retriever padrão
    será criado automaticamente.
    """

    if retriever is None:
        retriever = create_retriever()

    return RAG(
        retriever=retriever,
    )
