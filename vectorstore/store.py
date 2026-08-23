"""
Vector Store local para armazenamento e busca semântica dos chunks.

Responsabilidades:

    1. Armazenar embeddings dos chunks.
    2. Preservar texto e metadados.
    3. Persistir os dados em disco.
    4. Realizar busca por similaridade de cosseno.

Fluxo:

    Chunks
       ↓
    Embeddings
       ↓
    VectorStore
       ↓
    Similarity Search
       ↓
    Chunks relevantes
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


# ============================================================
# CONFIGURAÇÃO
# ============================================================

DEFAULT_VECTOR_STORE_PATH = Path(
    "data/vector_store/index.json"
)


# ============================================================
# VECTOR STORE
# ============================================================

class VectorStore:
    """
    Implementação local de um banco vetorial simples.

    Cada registro armazenado contém:

        - embedding
        - texto
        - metadados

    A similaridade é calculada utilizando similaridade de cosseno.
    """

    def __init__(
        self,
        path: str | Path = DEFAULT_VECTOR_STORE_PATH,
    ) -> None:
        """
        Inicializa o Vector Store.

        Parameters
        ----------
        path:
            Caminho do arquivo utilizado para persistência.
        """

        self.path = Path(path)

        self.documents: list[dict[str, Any]] = []

        self._load()

    # ========================================================
    # PERSISTÊNCIA
    # ========================================================

    def _load(self) -> None:
        """
        Carrega os documentos persistidos, caso existam.
        """

        if not self.path.exists():
            return

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "O Vector Store deve conter uma lista de documentos."
            )

        self.documents = data

    def save(self) -> None:
        """
        Persiste o Vector Store em disco.
        """

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.documents,
                file,
                ensure_ascii=False,
                indent=2,
            )

    # ========================================================
    # INSERÇÃO
    # ========================================================

    def add_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> None:
        """
        Adiciona documentos ao Vector Store.

        Cada documento deve possuir:

            - embedding
            - text

        Os demais campos são preservados como metadados.
        """

        if not isinstance(documents, list):
            raise TypeError(
                "documents deve ser uma lista."
            )

        for document in documents:

            if not isinstance(document, dict):
                raise TypeError(
                    "Cada documento deve ser um dicionário."
                )

            if "embedding" not in document:
                raise ValueError(
                    "Documento deve possuir o campo 'embedding'."
                )

            if "text" not in document:
                raise ValueError(
                    "Documento deve possuir o campo 'text'."
                )

            embedding = document["embedding"]

            if not isinstance(embedding, list):
                raise TypeError(
                    "embedding deve ser uma lista de números."
                )

            if not embedding:
                raise ValueError(
                    "embedding não pode estar vazio."
                )

            if not all(
                isinstance(value, (int, float))
                for value in embedding
            ):
                raise TypeError(
                    "embedding deve conter apenas números."
                )

            self.documents.append(
                document
            )

        self.save()


    # ========================================================
    # CONTAGEM
    # ========================================================

    def count(self) -> int:
        """
        Retorna a quantidade de documentos armazenados.
        """

        return len(self.documents)

    # ========================================================
    # LIMPEZA
    # ========================================================

    def clear(self) -> None:
        """
        Remove todos os documentos do Vector Store.
        """

        self.documents = []

        if self.path.exists():
            self.path.unlink()

    # ========================================================
    # BUSCA POR SIMILARIDADE
    # ========================================================

    @staticmethod
    def _cosine_similarity(
        query_vector: list[float],
        document_vector: list[float],
    ) -> float:
        """
        Calcula a similaridade de cosseno entre dois vetores.
        """

        query = np.asarray(
            query_vector,
            dtype=float,
        )

        document = np.asarray(
            document_vector,
            dtype=float,
        )

        if query.ndim != 1 or document.ndim != 1:
            raise ValueError(
                "Os embeddings devem ser vetores unidimensionais."
            )

        if query.shape != document.shape:
            raise ValueError(
                "Os embeddings devem possuir a mesma dimensão."
            )

        query_norm = np.linalg.norm(query)
        document_norm = np.linalg.norm(document)

        if query_norm == 0 or document_norm == 0:
            return 0.0

        return float(
            np.dot(query, document)
            / (query_norm * document_norm)
        )

    def similarity_search(
        self,
        query_embedding: list[float],
        k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Retorna os documentos mais similares à consulta.

        Parameters
        ----------
        query_embedding:
            Embedding da pergunta do usuário.

        k:
            Quantidade máxima de resultados.

        Returns
        -------
        list[dict[str, Any]]
            Documentos ordenados pela similaridade,
            do maior para o menor valor.
        """

        if not isinstance(
            query_embedding,
            list,
        ):
            raise TypeError(
                "query_embedding deve ser uma lista."
            )

        if not query_embedding:
            raise ValueError(
                "query_embedding não pode estar vazio."
            )

        if not isinstance(k, int):
            raise TypeError(
                "k deve ser um inteiro."
            )

        if k <= 0:
            raise ValueError(
                "k deve ser maior que zero."
            )

        if not self.documents:
            return []

        results = []

        for document in self.documents:

            similarity = self._cosine_similarity(
                query_embedding,
                document["embedding"],
            )

            result = {
                **document,
                "similarity": similarity,
            }

            results.append(result)

        results.sort(
            key=lambda item: item["similarity"],
            reverse=True,
        )

        return results[:k]


# ============================================================
# FACTORY
# ============================================================

def create_vector_store(
    path: str | Path = DEFAULT_VECTOR_STORE_PATH,
) -> VectorStore:
    """
    Cria uma instância do Vector Store.

    Parameters
    ----------
    path:
        Caminho para persistência.

    Returns
    -------
    VectorStore
        Instância configurada.
    """

    return VectorStore(path=path)