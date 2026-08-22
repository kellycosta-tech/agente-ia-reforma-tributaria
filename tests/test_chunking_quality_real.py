"""
Teste integrado de qualidade do Chunking utilizando o PDF oficial.

Fluxo:

    PDF
     ↓
    Extraction
     ↓
    Cleaning
     ↓
    Chunking
     ↓
    Análise de qualidade
     ↓
    Identificação de chunks problemáticos
     ↓
    Validação de termos críticos
"""

from pathlib import Path
from statistics import mean, median

from ingestion.extraction import extract_document
from ingestion.cleaning import clean_document
from ingestion.chunking import chunk_document


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "documentos"
    / "Modulo_1_parte_1.pdf"
)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

TEST_DOCUMENT_METADATA = {
    "document_id": "test-document-001",
    "document_name": "Modulo_1_parte_1.pdf",
    "document_type": "PDF",
    "source_organization": "CFC",
    "publication_date": None,
}

# ============================================================
# TESTE INTEGRADO
# ============================================================

def test_chunking_quality_real_pdf():

    # ========================================================
    # 1. EXTRACTION
    # ========================================================

    document = extract_document(
        PDF_PATH
    )

    assert len(document) == 63

    # ========================================================
    # 2. CLEANING
    # ========================================================

    cleaned_document = clean_document(
        document
    )

    assert len(cleaned_document) == 63

    # ========================================================
    # 3. CHUNKING
    # ========================================================

    chunks = chunk_document(
    cleaned_document,
    document_metadata=TEST_DOCUMENT_METADATA,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

    assert len(chunks) > 0

    # ========================================================
    # CABEÇALHO
    # ========================================================

    print("\n")
    print("=" * 70)
    print("📊 QUALIDADE DO CHUNKING — PDF OFICIAL")
    print("=" * 70)

    print(
        f"Páginas processadas : {len(cleaned_document)}"
    )

    print(
        f"Chunks gerados      : {len(chunks)}"
    )

    # ========================================================
    # 4. TAMANHO DOS CHUNKS
    # ========================================================

    char_counts = [
        chunk["char_count"]
        for chunk in chunks
    ]

    minimum = min(char_counts)
    maximum = max(char_counts)
    average = mean(char_counts)
    median_value = median(char_counts)

    print("\n")
    print("=" * 70)
    print("📏 TAMANHO DOS CHUNKS")
    print("=" * 70)

    print(
        f"Mínimo             : {minimum}"
    )

    print(
        f"Máximo             : {maximum}"
    )

    print(
        f"Média               : {average:.2f}"
    )

    print(
        f"Mediana             : {median_value:.2f}"
    )

    # ========================================================
    # 5. CHUNKS PEQUENOS
    # ========================================================

    small_chunks = [
        chunk
        for chunk in chunks
        if chunk["char_count"] < 200
    ]

    print("\n")
    print("=" * 70)
    print("📦 CHUNKS PEQUENOS")
    print("=" * 70)

    print(
        f"Chunks < 200 caracteres : "
        f"{len(small_chunks)}"
    )

    # ========================================================
    # 6. QUALITY SCORE
    # ========================================================

    high_quality = [
        chunk
        for chunk in chunks
        if chunk["quality_score"] >= 0.90
    ]

    medium_quality = [
        chunk
        for chunk in chunks
        if 0.70 <= chunk["quality_score"] < 0.90
    ]

    low_quality = [
        chunk
        for chunk in chunks
        if chunk["quality_score"] < 0.70
    ]

    print("\n")
    print("=" * 70)
    print("🧠 QUALITY SCORE")
    print("=" * 70)

    print(
        f"Score >= 0.90       : "
        f"{len(high_quality)}"
    )

    print(
        f"Score 0.70–0.89     : "
        f"{len(medium_quality)}"
    )

    print(
        f"Score < 0.70        : "
        f"{len(low_quality)}"
    )

    # ========================================================
    # 7. FLAGS
    # ========================================================

    numeric_heavy = [
        chunk
        for chunk in chunks
        if "numeric_heavy"
        in chunk["quality_flags"]
    ]

    heading_chunks = [
        chunk
        for chunk in chunks
        if "heading"
        in chunk["quality_flags"]
    ]

    short_chunks = [
        chunk
        for chunk in chunks
        if "short"
        in chunk["quality_flags"]
    ]

    print("\n")
    print("=" * 70)
    print("🚩 QUALITY FLAGS")
    print("=" * 70)

    print(
        f"numeric_heavy       : "
        f"{len(numeric_heavy)}"
    )

    print(
        f"heading             : "
        f"{len(heading_chunks)}"
    )

    print(
        f"short               : "
        f"{len(short_chunks)}"
    )

    # ========================================================
    # 8. CHUNKS PROBLEMÁTICOS
    # ========================================================

    problematic_chunks = [
        chunk
        for chunk in chunks
        if (
            chunk["quality_score"] < 0.70
            or "numeric_heavy"
            in chunk["quality_flags"]
            or "short"
            in chunk["quality_flags"]
        )
    ]

    print("\n")
    print("=" * 70)
    print("⚠️ CHUNKS QUE MERECEM REVISÃO")
    print("=" * 70)

    print(
        f"Total identificado : "
        f"{len(problematic_chunks)}"
    )

    # ========================================================
    # Mostra no máximo 10
    # ========================================================

    for chunk in problematic_chunks[:10]:

        print("\n")
        print(
            f"🧩 {chunk['chunk_id']}"
        )

        print(
            f"Página     : "
            f"{chunk['page']}"
        )

        print(
            f"Caracteres : "
            f"{chunk['char_count']}"
        )

        print(
            f"Score      : "
            f"{chunk['quality_score']}"
        )

        print(
            f"Flags      : "
            f"{chunk['quality_flags']}"
        )

        print("-" * 70)

        print(
            chunk["text"][:500]
        )

    # ========================================================
    # 9. TERMOS CRÍTICOS
    # ========================================================

    all_chunk_text = "\n".join(
        chunk["text"]
        for chunk in chunks
    )

    critical_terms = [
        "IVA DUAL",
        "EC 132/23",
        "LEI COMPLEMENTAR 214/25",
        "LEI COMPLEMENTAR 227/26",
        "FGTS",
        "MEI",
    ]

    print("\n")
    print("=" * 70)
    print("🛡️ TERMOS CRÍTICOS NOS CHUNKS")
    print("=" * 70)

    for term in critical_terms:

        found = term in all_chunk_text

        print(
            f"{'✅' if found else '❌'} "
            f"{term}"
        )

        assert found, (
            f"Termo crítico não encontrado: {term}"
        )

    # ========================================================
    # 10. VALIDAÇÃO DOS METADADOS
    # ========================================================

    for chunk in chunks:

        assert "chunk_id" in chunk

        assert "page" in chunk

        assert "chunk_index" in chunk

        assert "text" in chunk

        assert "char_count" in chunk

        assert "quality_score" in chunk

        assert "quality_flags" in chunk

        assert isinstance(
            chunk["text"],
            str,
        )

        assert isinstance(
            chunk["quality_flags"],
            list,
        )

        assert chunk["char_count"] == len(
            chunk["text"]
        )

    # ========================================================
    # 11. VALIDAÇÃO DOS IDs
    # ========================================================

    chunk_ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    assert len(chunk_ids) == len(
        set(chunk_ids)
    )

    # ========================================================
    # 12. VALIDAÇÃO DO SCORE
    # ========================================================

    for chunk in chunks:

        assert 0.0 <= chunk["quality_score"] <= 1.0

    # ========================================================
    # RESULTADO FINAL
    # ========================================================

    print("\n")
    print("=" * 70)
    print("✅ VALIDAÇÃO FINAL")
    print("=" * 70)

    print(
        "Extraction          : OK"
    )

    print(
        "Cleaning            : OK"
    )

    print(
        "Chunking            : OK"
    )

    print(
        "Quality Score       : OK"
    )

    print(
        "Metadados           : OK"
    )

    print(
        "IDs únicos          : OK"
    )

    print(
        "Termos críticos     : OK"
    )

    print("\n")
    print(
        "🎯 Qualidade do Chunking validada "
        "com o PDF oficial."
    )