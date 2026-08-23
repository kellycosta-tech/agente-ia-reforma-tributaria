"""
Reranker para reordenação dos resultados recuperados.

Responsabilidades:

    1. Receber uma pergunta.
    2. Receber candidatos recuperados pelo Retriever.
    3. Calcular a relevância pergunta × documento.
    4. Reordenar os candidatos.
    5. Retornar os resultados mais relevantes.
"""

from __future__ import annotations

from typing import Any

from sentence_transformers import CrossEncoder


# ============================================================
# CONFIGURAÇÃO
# ============================================================

DEFAULT_RERANKER_MODEL = (
    "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
)


# ============================================================
# MODELO
# ============================================================

def load_reranker_model(
    model_name: str = DEFAULT_RERANKER_MODEL,
) -> CrossEncoder:
    """
    Carrega o modelo Cross-Encoder utilizado no reranking.
    """

    return CrossEncoder(model_name)


# ============================================================
# RERANKING
# ============================================================

def rerank_results(
    query: str,
    results: list[dict[str, Any]],
    model: CrossEncoder,
    k: int = 5,
) -> list[dict[str, Any]]:
    """
    Reordena os resultados utilizando um Cross-Encoder.

    Parameters
    ----------
    query:
        Pergunta do usuário.

    results:
        Candidatos recuperados pelo Retriever.

    model:
        Modelo Cross-Encoder.

    k:
        Quantidade final de resultados.

    Returns
    -------
    list[dict[str, Any]]
        Resultados reordenados por relevância.
    """

    if not isinstance(query, str):
        raise TypeError("query deve ser uma string.")

    query = query.strip()

    if not query:
        raise ValueError("query não pode estar vazia.")

    if not isinstance(results, list):
        raise TypeError("results deve ser uma lista.")

    if not isinstance(k, int):
        raise TypeError("k deve ser um inteiro.")

    if k <= 0:
        raise ValueError("k deve ser maior que zero.")

    if not results:
        return []

    pairs = [
        (
            query,
            result.get("text", ""),
        )
        for result in results
    ]

    scores = model.predict(pairs)

    reranked_results = []

    for result, score in zip(results, scores):
        reranked_result = {
            **result,
            "rerank_score": float(score),
        }

        reranked_results.append(
            reranked_result
        )

    reranked_results.sort(
        key=lambda item: item["rerank_score"],
        reverse=True,
    )

    return reranked_results[:k]