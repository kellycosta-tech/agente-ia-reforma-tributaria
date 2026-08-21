"""
PDF Loader
==========

Responsabilidade:
    Carregar arquivos PDF e extrair seu conteúdo textual
    página por página.

Este módulo NÃO é responsável por:
    - limpeza;
    - chunking;
    - metadados;
    - embeddings;
    - vector store;
    - RAG.
"""

from pathlib import Path
from typing import Any

import pymupdf


def load_pdf(pdf_path: str | Path) -> list[dict[str, Any]]:
    """
    Extrai o texto de um PDF página por página.

    Parameters
    ----------
    pdf_path : str | Path
        Caminho do arquivo PDF.

    Returns
    -------
    list[dict[str, Any]]
        Lista contendo página e texto extraído.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Arquivo PDF não encontrado: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"O arquivo informado não é um PDF: {pdf_path}"
        )

    try:
        document = pymupdf.open(pdf_path)

    except Exception as exc:
        raise RuntimeError(
            f"Não foi possível abrir o PDF: {pdf_path}"
        ) from exc

    pages: list[dict[str, Any]] = []

    try:

        for page_number, page in enumerate(
            document,
            start=1
        ):

            text = page.get_text("text")

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

    finally:

        document.close()

    return pages


def get_pdf_page_count(
    pdf_path: str | Path
) -> int:
    """
    Retorna a quantidade de páginas do PDF.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Arquivo PDF não encontrado: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"O arquivo informado não é um PDF: {pdf_path}"
        )

    try:

        document = pymupdf.open(pdf_path)

        page_count = len(document)

        document.close()

        return page_count

    except Exception as exc:

        raise RuntimeError(
            f"Não foi possível obter o número de páginas: "
            f"{pdf_path}"
        ) from exc


def has_extractable_text(
    pdf_path: str | Path
) -> bool:
    """
    Verifica se o PDF possui texto extraível.

    Returns
    -------
    bool
        True  -> existe texto extraível.
        False -> provavelmente será necessário OCR.
    """

    pages = load_pdf(pdf_path)

    total_characters = sum(
        len(page["text"].strip())
        for page in pages
    )

    return total_characters > 0