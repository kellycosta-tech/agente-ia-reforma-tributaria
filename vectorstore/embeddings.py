"""
Geração de embeddings para os chunks documentais.

Responsabilidade:

    Transformar o texto dos chunks em vetores numéricos
    que possam ser utilizados pelo Vector Store.

Fluxo:

    Chunks
       ↓
    Embedding Model
       ↓
    Vetores
       ↓
    Vector Store
"""

from typing import Any

from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURAÇÃO
# ============================================================

DEFAULT_EMBEDDING_MODEL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# ============================================================
# MODELO
# ============================================================

def load_embedding_model(
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> SentenceTransformer:
    """
    Carrega o modelo responsável pela geração dos embeddings.

    Parameters
    ----------
    model_name:
        Nome do modelo Sentence Transformer.

    Returns
    -------
    SentenceTransformer
        Modelo carregado.
    """

    return SentenceTransformer(
        model_name
    )


# ============================================================
# EMBEDDING DE TEXTO
# ============================================================

def generate_embedding(
    text: str,
    model: SentenceTransformer,
) -> list[float]:
    """
    Gera o embedding de um texto.

    Parameters
    ----------
    text:
        Texto que será transformado em vetor.

    model:
        Modelo de embeddings.

    Returns
    -------
    list[float]
        Vetor numérico correspondente ao texto.
    """

    if not isinstance(text, str):
        raise TypeError(
            "text deve ser uma string."
        )

    text = text.strip()

    if not text:
        raise ValueError(
            "text não pode estar vazio."
        )

    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()


# ============================================================
# EMBEDDINGS DOS CHUNKS
# ============================================================

def generate_embeddings(
    chunks: list[dict[str, Any]],
    model: SentenceTransformer,
) -> list[dict[str, Any]]:
    """
    Gera embeddings para uma lista de chunks.

    Os metadados existentes são preservados.

    Parameters
    ----------
    chunks:
        Lista de chunks produzidos pelo Chunking.

    model:
        Modelo de embeddings.

    Returns
    -------
    list[dict[str, Any]]
        Chunks contendo o campo "embedding".
    """

    if not isinstance(chunks, list):
        raise TypeError(
            "chunks deve ser uma lista."
        )

    result = []

    for chunk in chunks:

        if not isinstance(chunk, dict):
            raise TypeError(
                "Cada chunk deve ser um dicionário."
            )

        if "text" not in chunk:
            raise ValueError(
                "Chunk deve possuir o campo 'text'."
            )

        embedding = generate_embedding(
            chunk["text"],
            model,
        )

        embedded_chunk = {
            **chunk,
            "embedding": embedding,
        }

        result.append(
            embedded_chunk
        )

    return result