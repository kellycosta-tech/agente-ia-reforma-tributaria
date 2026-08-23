"""
Retriever para recuperação semântica dos documentos.

Responsabilidades:

    1. Receber uma pergunta em linguagem natural.
    2. Gerar o embedding da pergunta.
    3. Consultar o Vector Store.
    4. Recuperar candidatos semanticamente relevantes.
    5. Aplicar filtros de metadados.
    6. Reordenar os candidatos utilizando um Reranker.
    7. Retornar os chunks mais relevantes.

Fluxo:

    Pergunta
       ↓
    Embedding Model
       ↓
    Query Embedding
       ↓
    Vector Store
       ↓
    Candidate Retrieval
       ↓
    Metadata Filters
       ↓
    Reranker
       ↓
    Top-K
"""

from __future__ import annotations

from typing import Any

from sentence_transformers import SentenceTransformer

from vectorstore.embeddings import (
    DEFAULT_EMBEDDING_MODEL,
    generate_embedding,
    load_embedding_model,
)

from vectorstore.reranker import (
    DEFAULT_RERANKER_MODEL,
    load_reranker_model,
    rerank_results,
)

from vectorstore.store import (
    DEFAULT_VECTOR_STORE_PATH,
    VectorStore,
)


# ============================================================
# RETRIEVER
# ============================================================

class Retriever:
    """
    Camada responsável pela recuperação semântica.

    O Retriever conecta:

        Embedding Model
              ↓
        Vector Store
              ↓
          Reranker
    """

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: SentenceTransformer,
        reranker_model: Any | None = None,
    ) -> None:
        """
        Inicializa o Retriever.

        Parameters
        ----------
        vector_store:
            Vector Store utilizado para recuperação.

        embedding_model:
            Modelo utilizado para gerar embeddings.

        reranker_model:
            Modelo utilizado para reordenar os resultados.
            É opcional para manter compatibilidade com testes
            e usos que não necessitam de reranking.
        """

        if not isinstance(
            vector_store,
            VectorStore,
        ):
            raise TypeError(
                "vector_store deve ser uma instância de VectorStore."
            )

        if not isinstance(
            embedding_model,
            SentenceTransformer,
        ):
            raise TypeError(
                "embedding_model deve ser uma instância de "
                "SentenceTransformer."
            )

        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.reranker_model = reranker_model

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
        Recupera os chunks mais relevantes para uma consulta.

        O processo ocorre em duas etapas:

        1. Recuperação semântica:
           busca um conjunto maior de candidatos no Vector Store.

        2. Reranking:
           reordena os candidatos utilizando um Cross-Encoder,
           quando um reranker está configurado.
        """

        # ----------------------------------------------------
        # VALIDAÇÃO DA QUERY
        # ----------------------------------------------------

        if not isinstance(
            query,
            str,
        ):
            raise TypeError(
                "query deve ser uma string."
            )

        query = query.strip()

        if not query:
            raise ValueError(
                "query não pode estar vazia."
            )

        # ----------------------------------------------------
        # VALIDAÇÃO DO K
        # ----------------------------------------------------

        if not isinstance(
            k,
            int,
        ):
            raise TypeError(
                "k deve ser um inteiro."
            )

        if k <= 0:
            raise ValueError(
                "k deve ser maior que zero."
            )

        # ----------------------------------------------------
        # GERAÇÃO DO EMBEDDING
        # ----------------------------------------------------

        query_embedding = generate_embedding(
            query,
            self.embedding_model,
        )

        # ----------------------------------------------------
        # RECUPERAÇÃO DE CANDIDATOS
        # ----------------------------------------------------

        # Recupera mais candidatos do que o necessário.
        #
        # Exemplo:
        #
        # k = 5
        # candidate_k = 20
        #
        # Isso fornece ao reranker um conjunto maior
        # de candidatos para selecionar os mais relevantes.

        candidate_k = max(
            k * 4,
            20,
        )

        results = self.vector_store.similarity_search(
            query_embedding,
            k=candidate_k,
        )

        # ----------------------------------------------------
        # FILTROS DE METADADOS
        # ----------------------------------------------------

        results = self.filter_results(
            results=results,
            source_organization=source_organization,
            module=module,
            document_name=document_name,
        )

        # ----------------------------------------------------
        # RERANKING
        # ----------------------------------------------------

        if self.reranker_model is not None:

            results = rerank_results(
                query=query,
                results=results,
                model=self.reranker_model,
                k=k,
            )

            return results

        # ----------------------------------------------------
        # FALLBACK SEM RERANKER
        # ----------------------------------------------------

        return results[:k]

    # ========================================================
    # FILTROS POR METADADOS
    # ========================================================

    def filter_results(
        self,
        results: list[dict[str, Any]],
        source_organization: str | None = None,
        module: str | None = None,
        document_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Filtra resultados recuperados utilizando metadados.

        Parameters
        ----------
        results:
            Resultados retornados pelo Vector Store.

        source_organization:
            Organização responsável pelo documento.

        module:
            Módulo do documento.

        document_name:
            Nome do documento.

        Returns
        -------
        list[dict[str, Any]]
            Resultados que atendem aos filtros informados.
        """

        if not isinstance(
            results,
            list,
        ):
            raise TypeError(
                "results deve ser uma lista."
            )

        filters = {
            "source_organization": source_organization,
            "module": module,
            "document_name": document_name,
        }

        for field, value in filters.items():

            if value is not None:

                if not isinstance(
                    value,
                    str,
                ):
                    raise TypeError(
                        f"{field} deve ser uma string."
                    )

                if not value.strip():
                    raise ValueError(
                        f"{field} não pode estar vazio."
                    )

        filtered_results = results

        if source_organization is not None:
            filtered_results = [
                result
                for result in filtered_results
                if result.get(
                    "source_organization"
                ) == source_organization
            ]

        if module is not None:
            filtered_results = [
                result
                for result in filtered_results
                if result.get(
                    "module"
                ) == module
            ]

        if document_name is not None:
            filtered_results = [
                result
                for result in filtered_results
                if result.get(
                    "document_name"
                ) == document_name
            ]

        return filtered_results


# ============================================================
# FACTORY
# ============================================================

def create_retriever(
    vector_store: VectorStore | None = None,
    embedding_model: SentenceTransformer | None = None,
    reranker_model: Any | None = None,
    vector_store_path: str = str(DEFAULT_VECTOR_STORE_PATH),
    embedding_model_name: str = DEFAULT_EMBEDDING_MODEL,
    reranker_model_name: str = DEFAULT_RERANKER_MODEL,
) -> Retriever:
    """
    Cria um Retriever configurado.
    """

    if vector_store is None:
        vector_store = VectorStore(
            path=vector_store_path,
        )

    if embedding_model is None:
        embedding_model = load_embedding_model(
            embedding_model_name,
        )

    if reranker_model is None:
        reranker_model = load_reranker_model(
            reranker_model_name,
        )

    return Retriever(
        vector_store=vector_store,
        embedding_model=embedding_model,
        reranker_model=reranker_model,
    )