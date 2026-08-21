"""
Testes do módulo Extraction.

Objetivo:
    Validar se o módulo extraction.py consegue:

    1. Localizar o documento.
    2. Identificar o formato.
    3. Utilizar o loader correto.
    4. Retornar o conteúdo estruturado.
    5. Rejeitar formatos inválidos.
    6. Identificar formatos previstos, mas ainda não implementados.
"""

from pathlib import Path

import pytest

from ingestion.extraction import extract_document


# =========================================================
# CONFIGURAÇÃO
# =========================================================

# Raiz do projeto.
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# Documento oficial utilizado nos testes.
PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "documentos"
    / "Modulo_1_parte_1.pdf"
)


# =========================================================
# TESTE 1 — PDF
# =========================================================

def test_extract_pdf():
    """
    Testa a extração de um PDF oficial.

    O documento utilizado possui 63 páginas.
    """

    document = extract_document(
        PDF_PATH
    )

    # Verifica se o resultado é uma lista.
    assert isinstance(
        document,
        list
    )

    # Verifica a quantidade esperada de páginas.
    assert len(document) == 63


# =========================================================
# TESTE 2 — ESTRUTURA
# =========================================================

def test_extracted_structure():
    """
    Verifica a estrutura retornada pelo Extraction.
    """

    document = extract_document(
        PDF_PATH
    )

    # O documento precisa possuir conteúdo.
    assert len(document) > 0

    # Obtém a primeira página.
    first_page = document[0]

    # Cada página deve possuir número.
    assert "page" in first_page

    # Cada página deve possuir texto.
    assert "text" in first_page


# =========================================================
# TESTE 3 — NUMERAÇÃO
# =========================================================

def test_page_number():
    """
    Verifica se a numeração das páginas
    foi preservada corretamente.
    """

    document = extract_document(
        PDF_PATH
    )

    # Primeira página.
    assert document[0]["page"] == 1

    # Segunda página.
    assert document[1]["page"] == 2


# =========================================================
# TESTE 4 — CONTEÚDO
# =========================================================

def test_pdf_content():
    """
    Verifica se o conteúdo textual
    foi preservado durante a extração.

    A página 2 contém "IVA DUAL".
    """

    document = extract_document(
        PDF_PATH
    )

    page_2_text = document[1]["text"]

    assert "IVA DUAL" in page_2_text


# =========================================================
# TESTE 5 — ARQUIVO INEXISTENTE
# =========================================================

def test_file_not_found():
    """
    Verifica se o Extraction gera
    FileNotFoundError quando o documento
    não existe.
    """

    invalid_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "documentos"
        / "arquivo_inexistente.pdf"
    )

    with pytest.raises(
        FileNotFoundError
    ):

        extract_document(
            invalid_path
        )


# =========================================================
# TESTE 6 — FORMATO DESCONHECIDO
# =========================================================

def test_unsupported_format(tmp_path):
    """
    Verifica se um formato desconhecido
    gera ValueError.

    Exemplo:
        .xyz
    """

    invalid_path = (
        tmp_path
        / "teste.xyz"
    )

    # Cria um arquivo temporário.
    invalid_path.write_text(
        "conteúdo de teste",
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match="Formato de arquivo não suportado"
    ):

        extract_document(
            invalid_path
        )


# =========================================================
# TESTE 7 — FORMATO PREVISTO, MAS NÃO IMPLEMENTADO
# =========================================================

def test_planned_but_not_implemented_format(tmp_path):
    """
    Verifica o comportamento para um formato
    previsto na arquitetura, mas cujo loader
    ainda não foi implementado.

    Exemplo:
        DOCX
    """

    docx_path = (
        tmp_path
        / "teste.docx"
    )

    # Cria um arquivo DOCX temporário.
    docx_path.write_text(
        "conteúdo de teste",
        encoding="utf-8"
    )

    with pytest.raises(
        NotImplementedError,
        match="está previsto na arquitetura"
    ):

        extract_document(
            docx_path
        )