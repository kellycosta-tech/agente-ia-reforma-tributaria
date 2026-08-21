"""
Testes da camada de Ingestion.

Responsabilidades testadas:

    1. PDF Loader
    2. Extraction

Os testes utilizam o PDF oficial da Reforma Tributária
armazenado em:

    data/raw/documentos/Modulo_1_parte_1.pdf
"""

from pathlib import Path

from ingestion.loaders.pdf_loader import (
    load_pdf,
    get_pdf_page_count,
    has_extractable_text,
)

from ingestion.extraction import extract_document


# =========================================================
# CONFIGURAÇÃO
# =========================================================

# Obtém a raiz do projeto independentemente
# de onde o pytest foi executado.
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# Caminho absoluto construído de forma segura.
PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "documentos"
    / "Modulo_1_parte_1.pdf"
)


# =========================================================
# TESTE 1 — PDF LOADER
# =========================================================

def test_pdf_loader():
    """
    Testa o carregamento básico do PDF.

    Valida:

        - quantidade de páginas;
        - existência de texto extraível;
        - carregamento das páginas.
    """

    # Verifica quantidade de páginas.
    page_count = get_pdf_page_count(
        PDF_PATH
    )

    assert page_count == 63

    # Verifica se existe texto extraível.
    assert has_extractable_text(
        PDF_PATH
    )

    # Carrega as páginas.
    pages = load_pdf(
        PDF_PATH
    )

    # Verifica se todas as 63 páginas foram carregadas.
    assert len(pages) == 63


# =========================================================
# TESTE 2 — EXTRACTION
# =========================================================

def test_extraction():
    """
    Testa a camada de Extraction.

    Valida:

        - quantidade de páginas;
        - estrutura do documento;
        - presença de page;
        - presença de text.
    """

    document = extract_document(
        PDF_PATH
    )

    # O documento possui 63 páginas.
    assert len(document) == 63

    # Verifica a estrutura da primeira página.
    assert "page" in document[0]

    assert "text" in document[0]