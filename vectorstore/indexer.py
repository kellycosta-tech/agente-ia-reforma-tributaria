"""
Indexador da base documental.

Fluxo:

PDF
    ↓
Pipeline de ingestão
    ↓
Chunks
    ↓
Embeddings
    ↓
Vector Store
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ingestion.pipeline import process_document

from vectorstore.embeddings import (
    generate_embeddings,
    load_embedding_model,
)

from vectorstore.store import (
    DEFAULT_VECTOR_STORE_PATH,
    VectorStore,
)


DEFAULT_DOCUMENTS_PATH = Path(
    "data/raw/documentos"
)


def index_documents(
    documents_path: str | Path = DEFAULT_DOCUMENTS_PATH,
    vector_store_path: str | Path = DEFAULT_VECTOR_STORE_PATH,
    source_organization: str = "CFC",
    publication_date: str | None = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> dict[str, Any]:
    """
    Processa os documentos e cria o Vector Store.

    Parameters
    ----------
    documents_path:
        Diretório contendo os PDFs.

    vector_store_path:
        Caminho do índice vetorial.

    source_organization:
        Organização responsável pelos documentos.

    publication_date:
        Data de publicação, quando disponível.

    chunk_size:
        Tamanho dos chunks.

    chunk_overlap:
        Sobreposição dos chunks.

    Returns
    -------
    dict
        Estatísticas da indexação.
    """

    documents_path = Path(documents_path)
    vector_store_path = Path(vector_store_path)

    if not documents_path.exists():
        raise FileNotFoundError(
            f"Diretório de documentos não encontrado: "
            f"{documents_path}"
        )

    pdf_files = sorted(
        [
            path
            for path in documents_path.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".pdf"
        ]
    )

    if not pdf_files:
        raise ValueError(
            f"Nenhum PDF encontrado em: "
            f"{documents_path}"
        )

    print("=" * 70)
    print("📚 INDEXAÇÃO DA BASE DOCUMENTAL")
    print("=" * 70)
    print(
        f"Documentos encontrados: {len(pdf_files)}"
    )

    # --------------------------------------------------------
    # 1. PROCESSAMENTO DOCUMENTAL
    # --------------------------------------------------------

    all_chunks: list[dict[str, Any]] = []

    for index, pdf_path in enumerate(
        pdf_files,
        start=1,
    ):

        print()
        print(
            f"[{index}/{len(pdf_files)}] "
            f"Processando: {pdf_path.name}"
        )

        document_id = (
            pdf_path.stem.lower()
            .replace(" ", "_")
        )

        result = process_document(
            file_path=pdf_path,
            document_id=document_id,
            document_name=pdf_path.name,
            document_type="PDF",
            source_organization=source_organization,
            publication_date=publication_date,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        chunks = result["chunking"]["chunks"]

        print(
            f"   Páginas: "
            f"{result['statistics']['pages_extracted']}"
        )

        print(
            f"   Chunks: {len(chunks)}"
        )

        all_chunks.extend(chunks)

    print()
    print("-" * 70)
    print(
        f"📦 Total de chunks: {len(all_chunks)}"
    )

    if not all_chunks:
        raise ValueError(
            "Nenhum chunk foi produzido pelo pipeline."
        )

    # --------------------------------------------------------
    # 2. EMBEDDINGS
    # --------------------------------------------------------

    print()
    print("🧠 Carregando modelo de embeddings...")

    embedding_model = load_embedding_model()

    print("🧠 Gerando embeddings...")

    embedded_chunks = generate_embeddings(
        all_chunks,
        embedding_model,
    )

    print(
        f"✅ Embeddings gerados: "
        f"{len(embedded_chunks)}"
    )

    # --------------------------------------------------------
    # 3. VECTOR STORE
    # --------------------------------------------------------

    print()
    print("💾 Criando Vector Store...")

    vector_store = VectorStore(
        path=vector_store_path
    )

    # Reconstrução limpa do índice.
    vector_store.clear()

    vector_store.add_documents(
        embedded_chunks
    )

    print(
        f"✅ Documentos indexados: "
        f"{vector_store.count()}"
    )

    print(
        f"📁 Índice: "
        f"{vector_store_path}"
    )

    # --------------------------------------------------------
    # 4. RESULTADO
    # --------------------------------------------------------

    statistics = {
        "documents": len(pdf_files),
        "chunks": len(all_chunks),
        "indexed": vector_store.count(),
        "vector_store": str(vector_store_path),
    }

    print()
    print("=" * 70)
    print("✅ INDEXAÇÃO CONCLUÍDA")
    print("=" * 70)

    print(
        f"Documentos: {statistics['documents']}"
    )

    print(
        f"Chunks: {statistics['chunks']}"
    )

    print(
        f"Vetores indexados: {statistics['indexed']}"
    )

    print(
        f"Vector Store: {statistics['vector_store']}"
    )

    return statistics


if __name__ == "__main__":

    index_documents()