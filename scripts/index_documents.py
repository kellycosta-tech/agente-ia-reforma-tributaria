"""
Indexação dos documentos no Vector Store.

Fluxo:

PDFs
  ↓
Ingestion Pipeline
  ↓
Chunks
  ↓
Embeddings
  ↓
Vector Store
"""

from __future__ import annotations

import sys
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO DO PROJETO
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# IMPORTS DO PROJETO
# ============================================================

from ingestion.pipeline import process_document
from vectorstore.embeddings import (
    generate_embeddings,
    load_embedding_model,
)
from vectorstore.store import create_vector_store


# ============================================================
# CAMINHOS
# ============================================================

DOCUMENTS_DIR = (
    BASE_DIR
    / "data"
    / "raw"
    / "documentos"
)

VECTOR_STORE_PATH = (
    BASE_DIR
    / "data"
    / "vector_store"
    / "index.json"
)


# ============================================================
# CONFIGURAÇÕES
# ============================================================

SOURCE_ORGANIZATION = "CFC"

DOCUMENT_TYPE = "PDF"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 150


# ============================================================
# INDEXAÇÃO
# ============================================================

def index_all_documents() -> None:

    print("=" * 70)
    print("📚 INDEXAÇÃO DOS DOCUMENTOS")
    print("=" * 70)

    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Diretório de documentos não encontrado: "
            f"{DOCUMENTS_DIR}"
        )

    pdf_files = sorted(
        [
            path
            for path in DOCUMENTS_DIR.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".pdf"
        ]
    )

    if not pdf_files:
        raise FileNotFoundError(
            f"Nenhum PDF encontrado em: {DOCUMENTS_DIR}"
        )

    print(
        f"📄 Documentos encontrados: {len(pdf_files)}"
    )

    # --------------------------------------------------------
    # Modelo de embeddings
    # --------------------------------------------------------

    print()
    print("🧠 Carregando modelo de embeddings...")

    embedding_model = load_embedding_model()

    print("✅ Modelo carregado.")

    # --------------------------------------------------------
    # Vector Store
    # --------------------------------------------------------

    vector_store = create_vector_store(
        path=VECTOR_STORE_PATH
    )

    # Evita duplicação em uma nova indexação
    vector_store.clear()

    print(
        f"🗂️ Vector Store: {VECTOR_STORE_PATH}"
    )

    # --------------------------------------------------------
    # Processamento
    # --------------------------------------------------------

    total_chunks = 0

    for index, pdf_path in enumerate(
        pdf_files,
        start=1,
    ):

        print()
        print(
            f"[{index}/{len(pdf_files)}] "
            f"Processando: {pdf_path.name}"
        )

        document_id = pdf_path.stem

        result = process_document(
            file_path=pdf_path,
            document_id=document_id,
            document_name=pdf_path.name,
            document_type=DOCUMENT_TYPE,
            source_organization=SOURCE_ORGANIZATION,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        chunks = result["chunking"]["chunks"]

        print(
            f"   📄 Páginas: "
            f"{result['statistics']['pages_extracted']}"
        )

        print(
            f"   🧩 Chunks: {len(chunks)}"
        )

        if not chunks:
            print("   ⚠️ Nenhum chunk criado.")
            continue

        # ----------------------------------------------------
        # Embeddings
        # ----------------------------------------------------

        embedded_chunks = generate_embeddings(
            chunks,
            embedding_model,
        )

        # ----------------------------------------------------
        # Vector Store
        # ----------------------------------------------------

        vector_store.add_documents(
            embedded_chunks
        )

        total_chunks += len(
            embedded_chunks
        )

        print("   ✅ Indexado.")

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("✅ INDEXAÇÃO CONCLUÍDA")
    print("=" * 70)

    print(
        f"📄 Documentos processados: "
        f"{len(pdf_files)}"
    )

    print(
        f"🧩 Chunks indexados: "
        f"{total_chunks}"
    )

    print(
        f"🗂️ Registros no Vector Store: "
        f"{vector_store.count()}"
    )

    print(
        f"💾 Índice salvo em:"
    )

    print(
        f"   {VECTOR_STORE_PATH}"
    )

    print("=" * 70)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    index_all_documents()