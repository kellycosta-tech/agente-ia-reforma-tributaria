"""
Testes do módulo Chunking.

Objetivo:

    Validar se o Chunking consegue:

    1. Dividir textos grandes.
    2. Preservar textos pequenos.
    3. Aplicar overlap.
    4. Validar parâmetros inválidos.
    5. Dividir uma página.
    6. Dividir um documento.
    7. Integrar Extraction + Cleaning + Chunking
       utilizando o PDF oficial de 63 páginas.
"""

from pathlib import Path

import pytest

from ingestion.chunking import (
    split_text,
    chunk_page,
    chunk_document,
)

from ingestion.extraction import extract_document
from ingestion.cleaning import clean_document


# =========================================================
# CONFIGURAÇÃO
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "documentos"
    / "Modulo_1_parte_1.pdf"
)


# =========================================================
# TESTE 1
# =========================================================

def test_split_text_small_text():
    """
    Verifica se um texto menor que o tamanho do chunk
    permanece como um único chunk.
    """

    text = (
        "A Reforma Tributária estabelece "
        "novas regras para a tributação."
    )

    chunks = split_text(
        text,
        chunk_size=1000,
        chunk_overlap=150,
    )

    assert len(chunks) == 1

    assert chunks[0] == text


# =========================================================
# TESTE 2
# =========================================================

def test_split_text_large_text():
    """
    Verifica se um texto grande é dividido
    em múltiplos chunks.
    """

    text = "Reforma Tributária " * 200

    chunks = split_text(
        text,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert len(chunks) > 1

    for chunk in chunks:

        assert isinstance(
            chunk,
            str,
        )

        assert len(chunk) > 0


# =========================================================
# TESTE 3
# =========================================================

def test_split_text_respects_chunk_size():
    """
    Verifica se os chunks respeitam o tamanho definido.
    """

    text = "Reforma Tributária " * 200

    chunk_size = 200

    chunks = split_text(
        text,
        chunk_size=chunk_size,
        chunk_overlap=30,
    )

    for chunk in chunks:

        assert len(chunk) <= chunk_size


# =========================================================
# TESTE 4
# =========================================================

def test_split_text_empty():
    """
    Verifica o comportamento para texto vazio.
    """

    chunks = split_text(
        "",
        chunk_size=1000,
        chunk_overlap=150,
    )

    assert chunks == []


# =========================================================
# TESTE 5
# =========================================================

def test_invalid_chunk_size():
    """
    Verifica se chunk_size inválido gera erro.
    """

    with pytest.raises(ValueError):

        split_text(
            "Texto de teste.",
            chunk_size=0,
            chunk_overlap=10,
        )


# =========================================================
# TESTE 6
# =========================================================

def test_invalid_overlap():
    """
    Verifica se overlap maior ou igual ao tamanho
    do chunk gera erro.
    """

    with pytest.raises(ValueError):

        split_text(
            "Texto de teste.",
            chunk_size=100,
            chunk_overlap=100,
        )


# =========================================================
# TESTE 7
# =========================================================

def test_chunk_page():
    """
    Verifica a divisão de uma página.
    """

    page = {
        "page": 10,
        "text": (
            "Reforma Tributária "
            * 100
        ),
    }

    chunks = chunk_page(
        page,
        chunk_size=200,
        chunk_overlap=30,
    )

    assert len(chunks) > 1

    for chunk in chunks:

        assert chunk["page"] == 10

        assert "chunk_index" in chunk

        assert "text" in chunk

        assert "char_count" in chunk

        assert isinstance(
            chunk["text"],
            str,
        )


# =========================================================
# TESTE 8
# =========================================================

def test_chunk_document():
    """
    Verifica a divisão de um documento com duas páginas.
    """

    document = [

        {
            "page": 1,
            "text": (
                "Reforma Tributária "
                * 100
            ),
        },

        {
            "page": 2,
            "text": (
                "IVA Dual "
                * 100
            ),
        },

    ]

    chunks = chunk_document(
        document,
        chunk_size=200,
        chunk_overlap=30,
    )

    assert len(chunks) > 1

    # Todos os chunks devem possuir ID.
    for chunk in chunks:

        assert "chunk_id" in chunk

        assert "page" in chunk

        assert "text" in chunk

        assert "chunk_index" in chunk

        assert "char_count" in chunk


# =========================================================
# TESTE 9
# =========================================================

def test_chunk_ids_are_unique():
    """
    Verifica se os IDs dos chunks são únicos.
    """

    document = [

        {
            "page": 1,
            "text": (
                "Reforma Tributária "
                * 100
            ),
        },

        {
            "page": 2,
            "text": (
                "IVA Dual "
                * 100
            ),
        },

    ]

    chunks = chunk_document(
        document,
        chunk_size=200,
        chunk_overlap=30,
    )

    chunk_ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    assert len(chunk_ids) == len(
        set(chunk_ids)
    )


# =========================================================
# TESTE 10 — INTEGRAÇÃO COM PDF REAL
# =========================================================

def test_chunking_real_pdf():
    """
    Teste integrado:

        PDF
         ↓
        Extraction
         ↓
        Cleaning
         ↓
        Chunking

    Utiliza o PDF oficial de 63 páginas.
    """

    # -----------------------------------------------------
    # Extraction
    # -----------------------------------------------------

    document = extract_document(
        PDF_PATH
    )

    assert len(document) == 63

    # -----------------------------------------------------
    # Cleaning
    # -----------------------------------------------------

    cleaned_document = clean_document(
        document
    )

    assert len(cleaned_document) == 63

    # -----------------------------------------------------
    # Chunking
    # -----------------------------------------------------

    chunks = chunk_document(
        cleaned_document,
        chunk_size=1000,
        chunk_overlap=150,
    )

    # -----------------------------------------------------
    # Valida existência de chunks
    # -----------------------------------------------------

    assert len(chunks) > 0

    # -----------------------------------------------------
    # Exibe informações
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("✂️ TESTE DE CHUNKING — PDF OFICIAL")
    print("=" * 70)

    print(
        f"Páginas processadas : "
        f"{len(cleaned_document)}"
    )

    print(
        f"Chunks gerados      : "
        f"{len(chunks)}"
    )

    # -----------------------------------------------------
    # Mostra os primeiros chunks
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("📦 PRIMEIROS CHUNKS")
    print("=" * 70)

    for chunk in chunks[:5]:

        print("\n")
        print(
            f"🧩 {chunk['chunk_id']}"
        )

        print(
            f"Página       : "
            f"{chunk['page']}"
        )

        print(
            f"Índice       : "
            f"{chunk['chunk_index']}"
        )

        print(
            f"Caracteres   : "
            f"{chunk['char_count']}"
        )

        print("-" * 70)

        print(
            chunk["text"][:500]
        )

    # -----------------------------------------------------
    # Validação estrutural
    # -----------------------------------------------------

    for chunk in chunks:

        assert "chunk_id" in chunk

        assert "page" in chunk

        assert "chunk_index" in chunk

        assert "text" in chunk

        assert "char_count" in chunk

        assert isinstance(
            chunk["text"],
            str,
        )

        assert len(
            chunk["text"]
        ) > 0

    # -----------------------------------------------------
    # IDs únicos
    # -----------------------------------------------------

    chunk_ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    assert len(chunk_ids) == len(
        set(chunk_ids)
    )

    # -----------------------------------------------------
    # Validação de conteúdo tributário
    # -----------------------------------------------------

    all_chunks_text = "\n".join(
        chunk["text"]
        for chunk in chunks
    )

    critical_terms = [

        "IVA DUAL",

        "EC 132/23",

        "LEI COMPLEMENTAR 214/25",

    ]

    print("\n")
    print("=" * 70)
    print("🛡️ TERMOS CRÍTICOS NOS CHUNKS")
    print("=" * 70)

    for term in critical_terms:

        found = (
            term in all_chunks_text
        )

        print(
            f"{'✅' if found else '❌'} "
            f"{term}"
        )

        assert found