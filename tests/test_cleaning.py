"""
Testes do módulo Cleaning.

Objetivo:
    Validar a limpeza do conteúdo extraído
    sem destruir informações importantes.
"""

from ingestion.cleaning import (
    normalize_whitespace,
    remove_page_number,
    remove_repeated_lines,
    clean_text,
    clean_document,
)


def test_normalize_whitespace():
    """
    Testa a normalização de espaços.
    """

    text = (
        "IVA    DUAL\n"
        "\n"
        "\n"
        "\n"
        "Tributação    sobre consumo"
    )

    result = normalize_whitespace(
        text
    )

    assert "IVA DUAL" in result

    assert "Tributação sobre consumo" in result

    assert "\n\n\n" not in result


def test_remove_page_number():
    """
    Testa a remoção de números de página isolados.
    """

    text = (
        "IVA DUAL\n"
        "Conteúdo tributário\n"
        "3"
    )

    result = remove_page_number(
        text
    )

    assert "IVA DUAL" in result

    assert "Conteúdo tributário" in result

    assert "\n3" not in result


def test_preserve_numbers_inside_text():
    """
    Garante que números importantes não sejam removidos.

    Exemplo:

        EC 132/23
        LC 214/25
        9%
    """

    text = (
        "EC 132/23\n"
        "LC 214/25\n"
        "Alíquota de 9%"
    )

    result = remove_page_number(
        text
    )

    assert "EC 132/23" in result

    assert "LC 214/25" in result

    assert "9%" in result


def test_remove_repeated_lines():
    """
    Testa remoção de linhas repetidas.
    """

    text = (
        "Reforma Tributária\n"
        "Conteúdo importante\n"
        "Reforma Tributária\n"
        "Outro conteúdo\n"
        "Reforma Tributária\n"
        "Informação final"
    )

    result = remove_repeated_lines(
        text
    )

    assert "Conteúdo importante" in result

    assert "Outro conteúdo" in result

    assert "Informação final" in result

    # A linha repetida deve ser removida.
    assert "Reforma Tributária" not in result


def test_clean_text():
    """
    Testa a limpeza completa.
    """

    text = (
        "IVA    DUAL\n"
        "Conteúdo tributário\n"
        "3"
    )

    result = clean_text(
        text
    )

    assert "IVA DUAL" in result

    assert "Conteúdo tributário" in result

    assert "\n3" not in result


def test_clean_document():
    """
    Testa a limpeza de um documento estruturado.
    """

    document = [
        {
            "page": 1,
            "text": (
                "IVA    DUAL\n"
                "Conteúdo\n"
                "1"
            ),
        },
        {
            "page": 2,
            "text": (
                "EC 132/23\n"
                "LC 214/25"
            ),
        },
    ]

    result = clean_document(
        document
    )

    assert len(result) == 2

    assert result[0]["page"] == 1

    assert "IVA DUAL" in result[0]["text"]

    assert "EC 132/23" in result[1]["text"]

    assert "LC 214/25" in result[1]["text"]