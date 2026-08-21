"""
Teste manual do PDF Loader.

Exibe no terminal:

    - quantidade de páginas;
    - se existe texto extraível;
    - quantidade de páginas carregadas;
    - conteúdo das primeiras páginas.
"""

from pathlib import Path

from ingestion.loaders.pdf_loader import (
    load_pdf,
    get_pdf_page_count,
    has_extractable_text,
)


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
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":

    print("\n📄 TESTE DE PDF")
    print("=" * 60)

    # Quantidade de páginas
    page_count = get_pdf_page_count(
        PDF_PATH
    )

    print(
        f"Quantidade de páginas: {page_count}"
    )

    # Verifica se existe texto extraível
    extractable = has_extractable_text(
        PDF_PATH
    )

    print(
        f"Possui texto extraível: {extractable}"
    )

    # Carrega as páginas
    pages = load_pdf(
        PDF_PATH
    )

    print(
        f"Páginas carregadas: {len(pages)}"
    )

    # Mostra as primeiras 3 páginas
    print("\n")
    print("📑 CONTEÚDO DAS PRIMEIRAS PÁGINAS")
    print("=" * 60)

    for page in pages[:3]:

        print("\n")
        print(
            f"📄 PÁGINA {page['page']}"
        )

        print("-" * 60)

        text = page["text"]

        if text.strip():

            print(
                text[:1000]
            )

        else:

            print(
                "[Página sem texto extraível]"
            )

    print("\n")
    print("✅ Teste manual concluído.")