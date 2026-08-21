"""
Cleaning
========

Responsabilidade:
    Limpar o texto extraído dos documentos antes
    da etapa de chunking.

Objetivo:
    Remover ruídos de extração sem destruir
    informações importantes para o domínio tributário.

O módulo NÃO é responsável por:

    - extração de PDF;
    - chunking;
    - metadados;
    - embeddings;
    - vector store;
    - RAG.

Fluxo:

    PDF Loader
        ↓
    Extraction
        ↓
    Cleaning
        ↓
    Chunking
"""


import re
from typing import Any


def normalize_whitespace(text: str) -> str:
    """
    Normaliza espaços e quebras de linha.

    Mantém a estrutura básica do texto, mas remove:

        - espaços duplicados;
        - espaços no início/fim das linhas;
        - múltiplas linhas vazias.

    Parameters
    ----------
    text : str
        Texto original.

    Returns
    -------
    str
        Texto normalizado.
    """

    if not text:
        return ""

    # Normaliza espaços e tabs.
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove espaços no início/fim das linhas.
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
    )

    # Reduz excesso de linhas vazias.
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def remove_page_number(
    text: str,
) -> str:
    """
    Remove números de página isolados.

    Exemplo:

        "Conteúdo da página"
        "3"

    O número isolado será removido.

    Observação:
        Não remove números que estejam no meio
        de frases, percentuais ou referências legais.
    """

    if not text:
        return ""

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:

        stripped = line.strip()

        # Remove somente linhas contendo
        # exclusivamente um número.
        if re.fullmatch(
            r"\d+",
            stripped
        ):
            continue

        cleaned_lines.append(
            line
        )

    return "\n".join(
        cleaned_lines
    )


def remove_repeated_lines(
    text: str,
    min_repetitions: int = 3,
) -> str:
    """
    Remove linhas que aparecem repetidamente
    no documento.

    Útil para:

        - cabeçalhos;
        - rodapés;
        - títulos repetidos.

    Uma linha só será considerada ruído quando
    aparecer pelo menos `min_repetitions` vezes.

    Essa abordagem é conservadora para evitar
    remover informações tributárias legítimas.
    """

    if not text:
        return ""

    lines = text.splitlines()

    normalized_lines = [
        line.strip()
        for line in lines
        if line.strip()
    ]

    frequencies: dict[str, int] = {}

    for line in normalized_lines:

        frequencies[line] = (
            frequencies.get(line, 0) + 1
        )

    repeated_lines = {
        line
        for line, count in frequencies.items()
        if count >= min_repetitions
    }

    cleaned_lines = []

    for line in lines:

        normalized = line.strip()

        if normalized in repeated_lines:
            continue

        cleaned_lines.append(
            line
        )

    return "\n".join(
        cleaned_lines
    )


def clean_text(
    text: str,
) -> str:
    """
    Executa a limpeza básica do texto.

    Ordem:

        1. Remove números de página isolados.
        2. Remove linhas repetidas.
        3. Normaliza espaços.
    """

    if not text:
        return ""

    text = remove_page_number(
        text
    )

    text = remove_repeated_lines(
        text
    )

    text = normalize_whitespace(
        text
    )

    return text


def clean_document(
    document: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Limpa um documento estruturado.

    Parameters
    ----------
    document : list[dict]
        Documento retornado pelo Extraction.

    Returns
    -------
    list[dict]
        Documento com texto limpo.

    Exemplo de entrada:

        [
            {
                "page": 1,
                "text": "Texto bruto..."
            }
        ]

    Exemplo de saída:

        [
            {
                "page": 1,
                "text": "Texto limpo..."
            }
        ]
    """

    cleaned_document = []

    for page in document:

        cleaned_page = page.copy()

        cleaned_page["text"] = clean_text(
            page.get(
                "text",
                ""
            )
        )

        cleaned_document.append(
            cleaned_page
        )

    return cleaned_document