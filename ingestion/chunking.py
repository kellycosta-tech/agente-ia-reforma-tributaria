"""
Chunking semântico dos documentos.

Responsabilidade:

    Transformar o conteúdo limpo em chunks semanticamente coerentes,
    preservando títulos, parágrafos e listas sempre que possível.

Fluxo:

    Documento limpo
          ↓
    Separação por parágrafos
          ↓
    Identificação de títulos e listas
          ↓
    Agrupamento semântico
          ↓
    Avaliação de qualidade
          ↓
    Chunks
"""

from __future__ import annotations

import re
from typing import Any

from ingestion.metadata import validate_document_metadata


# ============================================================
# CONFIGURAÇÕES
# ============================================================

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 150

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def split_into_paragraphs(text: str) -> list[str]:
    """
    Divide um texto em blocos preservando parágrafos.

    Parágrafos são separados por uma ou mais linhas vazias.
    """

    if not text or not text.strip():
        return []

    paragraphs = re.split(
        r"\n\s*\n",
        text.strip(),
    )

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]


def split_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """
    Divide um texto em chunks menores.

    Esta função representa a divisão genérica por tamanho.

    A divisão tenta respeitar palavras e evita cortar o texto
    no meio sempre que possível.

    Parameters
    ----------
    text:
        Texto que será dividido.

    chunk_size:
        Tamanho aproximado máximo do chunk.

    chunk_overlap:
        Quantidade aproximada de caracteres compartilhados
        entre chunks consecutivos.

    Returns
    -------
    list[str]
        Lista de chunks.
    """

    if not isinstance(text, str):
        raise TypeError(
            "text deve ser uma string."
        )

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size deve ser maior que zero."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap não pode ser negativo."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap deve ser menor que chunk_size."
        )

    text = text.strip()

    if not text:
        return []

    # Texto pequeno: não precisa dividir.
    if len(text) <= chunk_size:
        return [text]

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length,
        )

        # ----------------------------------------------------
        # Tenta encontrar uma quebra natural
        # ----------------------------------------------------

        if end < text_length:

            possible_breaks = [
                text.rfind("\n", start, end),
                text.rfind(" ", start, end),
            ]

            best_break = max(
                possible_breaks
            )

            # Só utiliza a quebra encontrada se ela
            # não estiver muito próxima do início.
            if best_break > start:

                end = best_break

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # ----------------------------------------------------
        # Calcula próxima posição considerando overlap
        # ----------------------------------------------------

        next_start = end - chunk_overlap

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


def is_heading(text: str) -> bool:
    """
    Identifica heurísticas simples de títulos.

    Exemplos:

        CONTEXTO LEGISLATIVO
        PRINCÍPIOS CONSTITUCIONAIS DA RTC
        IVA DUAL

    Não é uma classificação perfeita.
    É uma heurística inicial para melhorar o chunking.
    """

    text = text.strip()

    if not text:
        return False

    if len(text) > 120:
        return False

    if text.endswith(
        (".", ";", ":")
    ):
        return False

    words = text.split()

    if len(words) > 15:
        return False

    letters = [
        char
        for char in text
        if char.isalpha()
    ]

    if not letters:
        return False

    uppercase_ratio = (
        sum(
            char.isupper()
            for char in letters
        )
        / len(letters)
    )

    return uppercase_ratio >= 0.70


def is_list_item(text: str) -> bool:
    """
    Identifica itens de listas.
    """

    return bool(
        re.match(
            r"^(•|-|\*|\d+[.)])\s+",
            text.strip(),
        )
    )


def is_numeric_heavy(text: str) -> bool:
    """
    Identifica textos predominantemente numéricos.

    A análise é feita por linha.

    Isso ajuda a identificar conteúdos provenientes de:

        - gráficos;
        - tabelas;
        - indicadores;
        - séries numéricas.

    O conteúdo NÃO é removido.
    Apenas recebe a sinalização "numeric_heavy".
    """

    if not text or not text.strip():
        return False

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return False

    numeric_lines = 0

    for line in lines:

        normalized = (
            line
            .replace(",", "")
            .replace(".", "")
            .replace("%", "")
            .replace("-", "")
            .replace(" ", "")
        )

        if normalized.isdigit():
            numeric_lines += 1

    numeric_ratio = (
        numeric_lines
        / len(lines)
    )

    return numeric_ratio >= 0.50


def calculate_quality_score(
    text: str,
) -> float:
    """
    Calcula um score heurístico de qualidade.

    O score não representa qualidade semântica absoluta.

    Ele serve para identificar chunks potencialmente
    problemáticos antes da etapa de embeddings.
    """

    if not text.strip():
        return 0.0

    score = 1.0

    # --------------------------------------------------------
    # Conteúdo predominantemente numérico
    # --------------------------------------------------------

    if is_numeric_heavy(text):
        score -= 0.30

    # --------------------------------------------------------
    # Chunk muito pequeno
    # --------------------------------------------------------

    if len(text) < 50:
        score -= 0.10

    return max(
        0.0,
        round(score, 2),
    )


# ============================================================
# CRIAÇÃO DO CHUNK
# ============================================================

def create_chunk(
    text: str,
    page: int,
    chunk_index: int,
    document_metadata: dict[str, Any],
    section: str | None = None,
    topic: str | None = None,
) -> dict[str, Any]:
    """
    Cria um chunk padronizado com conteúdo,
    metadados documentais e indicadores de qualidade.
    """

    text = text.strip()

    flags = []

    # --------------------------------------------------------
    # FLAGS DE QUALIDADE
    # --------------------------------------------------------

    if is_numeric_heavy(text):
        flags.append("numeric_heavy")

    if is_heading(text):
        flags.append("heading")

    if len(text) < 50:
        flags.append("short")

    # --------------------------------------------------------
    # CHUNK
    # --------------------------------------------------------

    return {
        "chunk_id": f"chunk_{chunk_index:04d}",

        # Identificação documental
        "document_id": document_metadata["document_id"],
        "document_name": document_metadata["document_name"],
        "document_type": document_metadata["document_type"],
        "source_organization": document_metadata["source_organization"],
        "publication_date": document_metadata.get("publication_date"),
        "source_url": document_metadata.get("source_url"),

        # Localização e contexto
        "page": page,
        "section": section,
        "topic": topic,

        # Controle do chunk
        "chunk_index": chunk_index,

        # Conteúdo
        "text": text,
        "char_count": len(text),

        # Qualidade
        "quality_score": calculate_quality_score(text),
        "quality_flags": flags,
    }

# ============================================================
# CHUNKING DE UMA PÁGINA
# ============================================================

def chunk_page(
    page: dict[str, Any],
    document_metadata: dict[str, Any],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict[str, Any]]:
    """
    Divide uma página em chunks preservando contexto.

    Estratégia:

        página
           ↓
        parágrafos
           ↓
        títulos / listas
           ↓
        agrupamento semântico
           ↓
        split_text() quando necessário
           ↓
        chunks

    Parameters
    ----------
    page:
        Página extraída e limpa.

    chunk_size:
        Tamanho aproximado máximo do chunk.

    chunk_overlap:
        Quantidade de contexto reutilizado entre chunks.

    Returns
    -------
    list[dict[str, Any]]
        Lista de chunks estruturados.
    """

    # ========================================================
    # 1. VALIDAÇÃO
    # ========================================================

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size deve ser maior que zero."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap não pode ser negativo."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap deve ser menor que chunk_size."
        )



    # ========================================================
    # 2. DADOS DA PÁGINA
    # ========================================================

    text = page.get(
        "text",
        "",
    )

    page_number = page.get(
        "page",
        0,
    )

    # ========================================================
    # 2.1 METADADOS DO DOCUMENTO
    # ========================================================

    section = page.get("section")
    topic = page.get("topic")

    # ========================================================
    # 3. PARÁGRAFOS
    # ========================================================

    paragraphs = split_into_paragraphs(
        text
    )

    if not paragraphs:
        return []

    # ========================================================
    # 4. AGRUPAMENTO
    # ========================================================

    chunks = []

    current_parts = []

    current_length = 0

    for paragraph in paragraphs:

        paragraph_length = len(
            paragraph
        )

        # ====================================================
        # PARÁGRAFO MUITO GRANDE
        # ====================================================

        if paragraph_length > chunk_size:

            # Finaliza conteúdo acumulado.
            if current_parts:

                chunks.append(
                    "\n\n".join(
                        current_parts
                    )
                )

                current_parts = []

                current_length = 0

            # Divide o parágrafo grande.
            large_chunks = split_text(
                paragraph,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            chunks.extend(
                large_chunks
            )

            continue

        # ====================================================
        # TÍTULO
        # ====================================================

        if is_heading(paragraph):

            if current_parts:

                chunks.append(
                    "\n\n".join(
                        current_parts
                    )
                )

                current_parts = []

                current_length = 0

            current_parts.append(
                paragraph
            )

            current_length = (
                paragraph_length
            )

            continue

        # ====================================================
        # LISTA
        # ====================================================

        if is_list_item(paragraph):

            proposed_length = (
                current_length
                + paragraph_length
                + 2
            )

            if (
                current_parts
                and proposed_length > chunk_size
            ):

                chunks.append(
                    "\n\n".join(
                        current_parts
                    )
                )

                current_parts = []

                current_length = 0

            current_parts.append(
                paragraph
            )

            current_length += (
                paragraph_length
                + 2
            )

            continue

        # ====================================================
        # PARÁGRAFO NORMAL
        # ====================================================

        proposed_length = (
            current_length
            + paragraph_length
            + 2
        )

        if (
            current_parts
            and proposed_length > chunk_size
        ):

            chunks.append(
                "\n\n".join(
                    current_parts
                )
            )

            # ------------------------------------------------
            # OVERLAP
            # ------------------------------------------------

            overlap_parts = []

            overlap_length = 0

            for previous_part in reversed(
                current_parts
            ):

                part_length = (
                    len(previous_part)
                    + 2
                )

                if (
                    overlap_length
                    + part_length
                    > chunk_overlap
                ):
                    break

                overlap_parts.insert(
                    0,
                    previous_part
                )

                overlap_length += (
                    part_length
                )

            current_parts = (
                overlap_parts
                + [paragraph]
            )

            current_length = (
                overlap_length
                + paragraph_length
                + 2
            )

        else:

            current_parts.append(
                paragraph
            )

            current_length = (
                proposed_length
            )

    # ========================================================
    # 5. ÚLTIMO CHUNK
    # ========================================================

    if current_parts:

        chunks.append(
            "\n\n".join(
                current_parts
            )
        )

    # ========================================================
    # 6. CRIAÇÃO DOS OBJETOS
    # ========================================================

    result = []

    for index, chunk_text in enumerate(
        chunks
    ):

        result.append(
            create_chunk(
                text=chunk_text,
                page=page_number,
                chunk_index=index,
                document_metadata=document_metadata,
                section=section,
                topic=topic,
)
        )

    return result

# ============================================================
# CHUNKING DO DOCUMENTO
# ============================================================

def chunk_document(
    document: list[dict[str, Any]],
    document_metadata: dict[str, Any],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict[str, Any]]:

    # --------------------------------------------------------
    # Validação dos metadados
    # --------------------------------------------------------

    validate_document_metadata(
    document_metadata
)
    # --------------------------------------------------------
    # Validação
    # --------------------------------------------------------

    if not isinstance(document, list):
        raise TypeError(
            "document deve ser uma lista."
        )

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size deve ser maior que zero."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap não pode ser negativo."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap deve ser menor que chunk_size."
        )

    # --------------------------------------------------------
    # Processamento
    # --------------------------------------------------------

    chunks = []

    global_index = 0

    for page in document:

        page_chunks = chunk_page(
            page,
            document_metadata=document_metadata,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for chunk in page_chunks:
            global_index += 1

            chunk["chunk_id"] = (
                f"chunk_{global_index:04d}"
            )

            chunk["chunk_index"] = global_index

            chunks.append(chunk)

    return chunks