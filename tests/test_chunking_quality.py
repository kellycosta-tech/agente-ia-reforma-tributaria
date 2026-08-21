"""
Testes de qualidade do Chunking.
"""

from ingestion.chunking import (
    is_heading,
    is_list_item,
    is_numeric_heavy,
    calculate_quality_score,
)


def test_detect_heading():

    assert is_heading(
        "CONTEXTO LEGISLATIVO"
    )


def test_detect_list():

    assert is_list_item(
        "• Simplicidade"
    )


def test_detect_numeric_heavy():

    text = """
    0,23
    0,24
    0,25
    0,29
    0,31
    """

    assert is_numeric_heavy(text)


def test_quality_score():

    text = """
    CONTEXTO LEGISLATIVO

    EC 132, de 20 de dezembro de 2023.

    LC 214, de 16 de janeiro de 2025.
    """

    score = calculate_quality_score(
        text
    )

    assert 0 < score <= 1