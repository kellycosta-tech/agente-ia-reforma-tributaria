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
    Gera embeddings para uma lista de chunks utilizando processamento
    em lote.

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
        Lista de chunks contendo o campo "embedding".
    """

    if not isinstance(chunks, list):
        raise TypeError(
            "chunks deve ser uma lista."
        )

    if not isinstance(model, SentenceTransformer):
        raise TypeError(
            "model deve ser uma instância de SentenceTransformer."
        )

    if not chunks:
        return []

    texts: list[str] = []

    for chunk in chunks:

        if not isinstance(chunk, dict):
            raise TypeError(
                "Cada chunk deve ser um dicionário."
            )

        if "text" not in chunk:
            raise ValueError(
                "Chunk deve possuir o campo 'text'."
            )

        text = chunk["text"]

        if not isinstance(text, str):
            raise TypeError(
                "O campo 'text' deve ser uma string."
            )

        text = text.strip()

        if not text:
            raise ValueError(
                "O campo 'text' não pode estar vazio."
            )

        texts.append(text)

    # ========================================================
    # GERAÇÃO DOS EMBEDDINGS EM BATCH
    # ========================================================

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    # ========================================================
    # REASSOCIA EMBEDDINGS AOS CHUNKS
    # ========================================================

    result: list[dict[str, Any]] = []

    for chunk, embedding in zip(
        chunks,
        embeddings,
    ):
        embedded_chunk = {
            **chunk,
            "embedding": embedding.tolist(),
        }

        result.append(
            embedded_chunk
        )

    return result