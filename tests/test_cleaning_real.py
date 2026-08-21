"""
Teste integrado do Cleaning utilizando o PDF oficial.

Fluxo:

    PDF
     ↓
    Extraction
     ↓
    Cleaning
     ↓
    Comparação ANTES x DEPOIS
     ↓
    Métricas
     ↓
    Análise do conteúdo removido
     ↓
    Validação de termos críticos
"""

from pathlib import Path

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
# TESTE INTEGRADO
# =========================================================

def test_cleaning_real_pdf():

    # =====================================================
    # 1. EXTRACTION
    # =====================================================

    document = extract_document(
        PDF_PATH
    )

    assert len(document) == 63

    # =====================================================
    # 2. CLEANING
    # =====================================================

    cleaned_document = clean_document(
        document
    )

    assert len(cleaned_document) == 63

    # =====================================================
    # 3. COMPARAÇÃO ANTES x DEPOIS
    # =====================================================

    print("\n")
    print("=" * 70)
    print("🧹 COMPARAÇÃO DO CLEANING")
    print("=" * 70)

    # Mostra somente as 3 primeiras páginas.
    # O processamento continua sendo realizado
    # nas 63 páginas.

    for original, cleaned in zip(
        document[:3],
        cleaned_document[:3],
    ):

        page_number = original["page"]

        original_text = original["text"]

        cleaned_text = cleaned["text"]

        print("\n")
        print(
            f"📄 PÁGINA {page_number}"
        )

        print("-" * 70)

        print("🔴 ANTES DA LIMPEZA")
        print("-" * 70)

        print(
            original_text[:500]
        )

        print("\n")

        print("🟢 DEPOIS DA LIMPEZA")
        print("-" * 70)

        print(
            cleaned_text[:500]
        )

    # =====================================================
    # 4. MÉTRICAS DA LIMPEZA
    # =====================================================

    original_chars = sum(
        len(page["text"])
        for page in document
    )

    cleaned_chars = sum(
        len(page["text"])
        for page in cleaned_document
    )

    removed_chars = (
        original_chars
        - cleaned_chars
    )

    print("\n")
    print("=" * 70)
    print("📊 RESULTADO DA LIMPEZA")
    print("=" * 70)

    print(
        f"Caracteres antes    : {original_chars:,}"
    )

    print(
        f"Caracteres depois   : {cleaned_chars:,}"
    )

    print(
        f"Caracteres removidos: {removed_chars:,}"
    )

    # -----------------------------------------------------
    # Percentual de redução
    # -----------------------------------------------------

    if original_chars > 0:

        reduction = (
            removed_chars
            / original_chars
        ) * 100

    else:

        reduction = 0

    print(
        f"Redução do conteúdo : {reduction:.2f}%"
    )

    # =====================================================
    # 5. PÁGINAS ALTERADAS
    # =====================================================

    changed_pages = 0

    for original, cleaned in zip(
        document,
        cleaned_document,
    ):

        if original["text"] != cleaned["text"]:

            changed_pages += 1

    unchanged_pages = (
        len(document)
        - changed_pages
    )

    changed_percentage = (
        changed_pages
        / len(document)
    ) * 100

    print("\n")
    print("=" * 70)
    print("📄 PÁGINAS ALTERADAS")
    print("=" * 70)

    print(
        f"Páginas analisadas : {len(document)}"
    )

    print(
        f"Páginas alteradas  : {changed_pages}"
    )

    print(
        f"Páginas preservadas: {unchanged_pages}"
    )

    print(
        f"Taxa de alteração  : "
        f"{changed_percentage:.2f}%"
    )

    # =====================================================
    # 6. ANÁLISE DO CONTEÚDO REMOVIDO
    # =====================================================

    removed_lines = []

    for original, cleaned in zip(
        document,
        cleaned_document,
    ):

        original_lines = set(
            line.strip()
            for line in original["text"].splitlines()
            if line.strip()
        )

        cleaned_lines = set(
            line.strip()
            for line in cleaned["text"].splitlines()
            if line.strip()
        )

        removed = (
            original_lines
            - cleaned_lines
        )

        for line in removed:

            removed_lines.append(
                {
                    "page": original["page"],
                    "text": line,
                }
            )

    print("\n")
    print("=" * 70)
    print("🔎 ANÁLISE DO CONTEÚDO REMOVIDO")
    print("=" * 70)

    print(
        f"Linhas removidas: {len(removed_lines)}"
    )

    print("\n")

    # Mostra no máximo 30 linhas.
    for item in removed_lines[:30]:

        print(
            f"Página {item['page']:>2}: "
            f"{item['text']}"
        )

    # =====================================================
    # 7. VALIDAÇÃO DA ESTRUTURA
    # =====================================================

    for page in cleaned_document:

        assert "page" in page

        assert "text" in page

        assert isinstance(
            page["text"],
            str
        )

    # =====================================================
    # 8. VALIDAÇÃO DO CONTEÚDO TRIBUTÁRIO
    # =====================================================

    all_text = "\n".join(
        page["text"]
        for page in cleaned_document
    )

    assert "IVA DUAL" in all_text

    assert "EC 132/23" in all_text

    assert "LEI COMPLEMENTAR 214/25" in all_text

    # =====================================================
    # 9. TERMOS CRÍTICOS PRESERVADOS
    # =====================================================

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
    print("🛡️ VALIDAÇÃO DE TERMOS CRÍTICOS")
    print("=" * 70)

    for term in critical_terms:

        found = term in all_text

        print(
            f"{'✅' if found else '❌'} {term}"
        )

        assert found