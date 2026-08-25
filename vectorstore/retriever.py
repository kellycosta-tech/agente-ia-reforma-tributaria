"""
Retriever para recuperação híbrida dos documentos.

Responsabilidades:

    1. Receber uma pergunta em linguagem natural.
    2. Gerar o embedding da pergunta.
    3. Consultar o Vector Store por similaridade semântica.
    4. Realizar busca lexical por termos relevantes.
    5. Combinar os candidatos.
    6. Aplicar filtros de metadados.
    7. Reordenar os candidatos utilizando um Reranker.
    8. Retornar os chunks mais relevantes.

Fluxo:

    Pergunta
       ↓
    ┌───────────────────────┐
    │ Busca Semântica        │
    │ Busca Lexical          │
    └───────────┬───────────┘
                ↓
        Candidatos Combinados
                ↓
        Filtros de Metadados
                ↓
             Reranker
                ↓
              Top-K
"""

from __future__ import annotations

import re
import unicodedata

from typing import Any

from sentence_transformers import SentenceTransformer

from vectorstore.embeddings import (
    DEFAULT_EMBEDDING_MODEL,
    generate_query_embedding,
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
    Camada responsável pela recuperação híbrida.

    Combina:

        Busca Semântica
              +
        Busca Lexical
              ↓
        Reranking
    """

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: SentenceTransformer,
        reranker_model: Any | None = None,
    ) -> None:
        """
        Inicializa o Retriever.
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

        Fluxo:

            Pergunta
                ↓
            Busca Semântica
                +
            Busca Lexical
                ↓
            Combinação
                ↓
            Filtros
                ↓
            Seleção ampliada de candidatos
                ↓
            Reranking
                ↓
            Top-K
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

        query_embedding = generate_query_embedding(
            query,
            self.embedding_model,
        )

        # ----------------------------------------------------
        # BUSCA SEMÂNTICA
        # ----------------------------------------------------

        semantic_k = max(
            k * 20,
            100,
        )

        semantic_results = (
            self.vector_store.similarity_search(
                query_embedding,
                k=semantic_k,
            )
        )

        # ----------------------------------------------------
        # BUSCA LEXICAL
        # ----------------------------------------------------

        lexical_results = self.lexical_search(
            query=query,
        )

        # ----------------------------------------------------
        # COMBINAÇÃO
        # ----------------------------------------------------

        combined_results = self.combine_results(
            semantic_results=semantic_results,
            lexical_results=lexical_results,
        )

        # ----------------------------------------------------
        # FILTROS DE METADADOS
        # ----------------------------------------------------

        combined_results = self.filter_results(
            results=combined_results,
            source_organization=source_organization,
            module=module,
            document_name=document_name,
        )

        # ----------------------------------------------------
        # RERANKING
        # ----------------------------------------------------

        if self.reranker_model is not None:

            # ------------------------------------------------
            # SELEÇÃO AMPLIADA DE CANDIDATOS
            #
            # O problema anterior era:
            #
            #     combined_results[:50]
            #
            # A página 22 estava na posição 127.
            #
            # Agora ampliamos o conjunto para permitir que
            # candidatos lexicais importantes cheguem ao
            # Cross-Encoder.
            # ------------------------------------------------

            rerank_k = max(
                k * 20,
                200,
            )

            # ------------------------------------------------
            # CANDIDATOS SEMÂNTICOS
            # ------------------------------------------------

            semantic_candidates = combined_results[
                :rerank_k
            ]

            # ------------------------------------------------
            # CANDIDATOS LEXICAIS
            #
            # Mantém os resultados encontrados diretamente
            # pelos termos da pergunta.
            # ------------------------------------------------

            lexical_candidates = [
                result
                for result in combined_results
                if result.get(
                    "lexical_score"
                ) is not None
            ]

            # ------------------------------------------------
            # UNIÃO DOS CANDIDATOS
            #
            # Evita duplicação utilizando _result_key().
            # ------------------------------------------------

            candidates: list[dict[str, Any]] = []

            candidate_keys: set[str] = set()

            for result in semantic_candidates:

                key = self._result_key(
                    result
                )

                if key not in candidate_keys:

                    candidate_keys.add(key)

                    candidates.append(
                        result
                    )

            for result in lexical_candidates:

                key = self._result_key(
                    result
                )

                if key not in candidate_keys:

                    candidate_keys.add(key)

                    candidates.append(
                        result
                    )

            # ------------------------------------------------
            # RERANKING
            # ------------------------------------------------

            reranked_results = rerank_results(
                query=query,
                results=candidates,
                model=self.reranker_model,
                k=len(candidates),
            )

            # ------------------------------------------------
            # AJUSTE DE RELEVÂNCIA LEXICAL
            #
            # O Cross-Encoder pode atribuir score baixo para
            # documentos que possuem a sigla correta.
            #
            # Para perguntas técnicas como:
            #
            #     "O que é o IBS?"
            #
            # a presença explícita de "IBS" deve ter peso.
            # ------------------------------------------------

            query_normalized = self._normalize_text(
                query
            )

            query_terms = self._extract_terms(
                query_normalized
            )

            for result in reranked_results:

                rerank_score = result.get(
                    "rerank_score",
                    0.0,
                )

                lexical_score = result.get(
                    "lexical_score"
                )

                lexical_bonus = 0.0
                acronym_bonus = 0.0

                # --------------------------------------------
                # BONUS LEXICAL
                # --------------------------------------------

                if lexical_score is not None:

                    lexical_bonus = min(
                        lexical_score / 2.0,
                        5.0,
                    )

                # --------------------------------------------
                # BONUS PARA SIGLAS/TERMOS DA QUERY
                # --------------------------------------------

                text = result.get(
                    "text",
                    "",
                )

                normalized_text = self._normalize_text(
                    text
                )

                for term in query_terms:

                    if (
                        len(term) <= 5
                        and term in normalized_text
                    ):
                        acronym_bonus += 1.5

                # --------------------------------------------
                # SCORE FINAL
                # --------------------------------------------

                result["lexical_bonus"] = (
                    lexical_bonus
                )

                result["acronym_bonus"] = (
                    acronym_bonus
                )

                result["final_score"] = (
                    rerank_score
                    + lexical_bonus
                    + acronym_bonus
                )

            # ------------------------------------------------
            # ORDENAÇÃO FINAL
            # ------------------------------------------------

            reranked_results.sort(
                key=lambda item: item.get(
                    "final_score",
                    item.get(
                        "rerank_score",
                        float("-inf"),
                    ),
                ),
                reverse=True,
            )

            return reranked_results[:k]

        # ----------------------------------------------------
        # FALLBACK SEM RERANKER
        # ----------------------------------------------------

        return combined_results[:k]


    # ========================================================
    # BUSCA LEXICAL
    # ========================================================

    def lexical_search(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        """
        Realiza uma busca lexical simples nos textos
        armazenados no Vector Store.

        A busca considera:

            - expressão exata da consulta;
            - termos relevantes;
            - siglas e termos técnicos.

        Returns
        -------
        list[dict[str, Any]]
            Documentos encontrados lexicalmente.
        """

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
        # NORMALIZAÇÃO
        # ----------------------------------------------------

        query_normalized = self._normalize_text(
            query
        )

        # ----------------------------------------------------
        # TERMOS DA CONSULTA
        # ----------------------------------------------------

        terms = self._extract_terms(
            query_normalized
        )

        if not terms:
            return []

        # ----------------------------------------------------
        # BUSCA NOS DOCUMENTOS
        # ----------------------------------------------------

        matches: list[dict[str, Any]] = []

        for document in self.vector_store.documents:

            text = document.get(
                "text",
                "",
            )

            if not isinstance(
                text,
                str,
            ):
                continue

            normalized_text = self._normalize_text(
                text
            )

            score = 0

            # ------------------------------------------------
            # EXPRESSÃO EXATA
            # ------------------------------------------------

            if (
                query_normalized
                and query_normalized in normalized_text
            ):
                score += 100

            # ------------------------------------------------
            # TERMOS INDIVIDUAIS
            # ------------------------------------------------

            for term in terms:

                if term in normalized_text:

                    # Siglas recebem peso maior.
                    if len(term) <= 5:
                        score += 10
                    else:
                        score += 3

            if score > 0:

                result = {
                    **document,
                    "lexical_score": score,
                }

                matches.append(
                    result
                )

        # ----------------------------------------------------
        # ORDENAÇÃO
        # ----------------------------------------------------

        matches.sort(
            key=lambda item: item[
                "lexical_score"
            ],
            reverse=True,
        )

        return matches
    # ========================================================
    # COMBINAÇÃO
    # ========================================================

    def combine_results(
        self,
        semantic_results: list[dict[str, Any]],
        lexical_results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Combina resultados semânticos e lexicais.

        Quando o mesmo chunk aparece nas duas buscas,
        mantém um único resultado e preserva os scores
        das duas estratégias de recuperação.
        """

        combined: list[dict[str, Any]] = []

        positions: dict[str, int] = {}

        # ----------------------------------------------------
        # RESULTADOS SEMÂNTICOS
        # ----------------------------------------------------

        for result in semantic_results:

            key = self._result_key(
                result
            )

            if key not in positions:

                positions[key] = len(
                    combined
                )

                combined.append(
                    dict(result)
                )

        # ----------------------------------------------------
        # RESULTADOS LEXICAIS
        # ----------------------------------------------------

        for result in lexical_results:

            key = self._result_key(
                result
            )

            if key in positions:

                index = positions[key]

                existing = combined[index]

                if result.get(
                    "lexical_score"
                ) is not None:

                    existing[
                        "lexical_score"
                    ] = result[
                        "lexical_score"
                    ]

                if result.get(
                    "similarity"
                ) is not None:

                    existing[
                        "similarity"
                    ] = result[
                        "similarity"
                    ]

            else:

                positions[key] = len(
                    combined
                )

                combined.append(
                    dict(result)
                )

        return combined

    # ========================================================
    # CHAVE DO RESULTADO
    # ========================================================

    @staticmethod
    def _result_key(
        result: dict[str, Any],
    ) -> str:
        """
        Cria uma chave estável e única para identificar um chunk.

        O chunk_id é reiniciado em cada documento. Por isso,
        ele não pode ser utilizado isoladamente como identificador.
        """

        document_id = result.get(
            "document_id"
        )

        chunk_id = result.get(
            "chunk_id"
        )

        if document_id is not None and chunk_id is not None:
            return (
                f"{document_id}|{chunk_id}"
            )

        return (
            f"{result.get('document_name', '')}|"
            f"{result.get('page', '')}|"
            f"{result.get('chunk_index', '')}"
        )

    # ========================================================
    # NORMALIZAÇÃO
    # ========================================================

    @staticmethod
    def _normalize_text(
        text: str,
    ) -> str:
        """
        Normaliza texto para busca lexical.

        Remove diferenças de maiúsculas/minúsculas,
        acentuação e espaços duplicados.
        """

        if not isinstance(text, str):
            return ""

        text = text.lower()

        text = unicodedata.normalize(
            "NFKD",
            text,
        )

        text = "".join(
            char
            for char in text
            if not unicodedata.combining(char)
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()
        
    # ========================================================
    # EXTRAÇÃO DE TERMOS
    # ========================================================

    @staticmethod
    def _extract_terms(
        query: str,
    ) -> list[str]:
        """
        Extrai termos relevantes da consulta.

        Remove palavras muito comuns e preserva
        siglas e termos técnicos.
        """

        words = re.findall(
            r"\b[\w-]+\b",
            query.lower(),
        )

        stopwords = {
            "o",
            "a",
            "os",
            "as",
            "um",
            "uma",
            "uns",
            "umas",
            "de",
            "da",
            "do",
            "das",
            "dos",
            "e",
            "ou",
            "em",
            "no",
            "na",
            "nos",
            "nas",
            "para",
            "por",
            "com",
            "sobre",
            "que",
            "é",
            "ser",
            "são",
            "qual",
            "quais",
            "como",
            "onde",
            "quando",
            "quem",
            "se",
        }

        return [
            word
            for word in words
            if word not in stopwords
            and len(word) >= 2
        ]
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
        Filtra resultados utilizando metadados.
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
    vector_store_path: str = str(
        DEFAULT_VECTOR_STORE_PATH
    ),
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