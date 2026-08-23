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
    Inferência de contexto estrutural
        ↓
    Agrupamento semântico
        ↓
    Avaliação de qualidade
        ↓
    Chunks

O módulo NÃO é responsável por:

    - extração de PDF;
    - limpeza documental;
    - geração de embeddings;
    - armazenamento vetorial;
    - recuperação semântica;
    - geração de respostas.
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
    Divide o texto extraído em blocos semanticamente úteis.

    Estratégia:
    1. Normaliza quebras de linha;
    2. Preserva listas e itens enumerados;
    3. Identifica títulos em linhas próprias;
    4. Identifica artigos em linhas próprias;
    5. Preserva parágrafos separados por linhas vazias;
    6. Evita transformar toda a página em um único bloco.

    Returns
    -------
    list[str]
        Lista de blocos textuais.
    """

    if not isinstance(text, str):
        raise TypeError("text deve ser uma string.")

    if not text.strip():
        return []

    # --------------------------------------------------------
    # 1. Normalização
    # --------------------------------------------------------

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        # Ignora números isolados que normalmente
        # representam paginação/rodapé do PDF.
        if re.fullmatch(r"\d{1,4}", line):
            continue

        lines.append(line)

    if not lines:
        return []

    paragraphs: list[str] = []
    current_lines: list[str] = []

    # --------------------------------------------------------
    # 2. Padrões estruturais
    # --------------------------------------------------------

    list_pattern = re.compile(
        r"^(?:[a-z]\)|\d+[.)]|[•\-*])\s+",
        re.IGNORECASE,
    )

    article_pattern = re.compile(
        r"^Art\.\s*\d+",
        re.IGNORECASE,
    )

    heading_pattern = re.compile(
        r"^[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ0-9][A-ZÁÀÂÃÉÊÍÓÔÕÚÇ0-9\s\-–—/()ºª.,]*$"
    )

    # --------------------------------------------------------
    # 3. Processamento linha a linha
    # --------------------------------------------------------

    for line in lines:

        is_list = bool(list_pattern.match(line))
        is_article = bool(article_pattern.match(line))

        is_heading_line = (
            len(line) <= 120
            and len(line.split()) <= 15
            and bool(heading_pattern.match(line))
            and not line.endswith((".", ";", ":"))
        )

        # ----------------------------------------------------
        # Título / heading
        # ----------------------------------------------------

        if is_heading_line:

            if current_lines:
                paragraphs.append(
                    " ".join(current_lines).strip()
                )
                current_lines = []

            paragraphs.append(line)
            continue

        # ----------------------------------------------------
        # Artigo
        # ----------------------------------------------------

        if is_article:

            if current_lines:
                paragraphs.append(
                    " ".join(current_lines).strip()
                )
                current_lines = []

            current_lines.append(line)
            continue

        # ----------------------------------------------------
        # Item de lista
        # ----------------------------------------------------

        if is_list:

            if current_lines:
                paragraphs.append(
                    " ".join(current_lines).strip()
                )
                current_lines = []

            current_lines.append(line)
            continue

        # ----------------------------------------------------
        # Continuação de texto
        # ----------------------------------------------------

        current_lines.append(line)

    # --------------------------------------------------------
    # 4. Último bloco
    # --------------------------------------------------------

    if current_lines:
        paragraphs.append(
            " ".join(current_lines).strip()
        )

    return [
        paragraph
        for paragraph in paragraphs
        if paragraph
    ]


def split_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """
    Divide um texto em chunks menores.

    A divisão tenta respeitar palavras e quebras naturais,
    evitando cortes desnecessários no meio do texto.

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

    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []

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
    Identifica títulos e subtítulos utilizando heurísticas
    estruturais.

    Exemplos:

        IMUNIDADES NA LEI COMPLEMENTAR 214
        Das Imunidades
        CONTEXTO LEGISLATIVO
        PRINCÍPIOS CONSTITUCIONAIS DA RTC
        IVA DUAL

    A função utiliza múltiplas heurísticas para reconhecer
    títulos em documentos jurídicos e institucionais.
    """

    text = text.strip()

    if not text:
        return False

    # --------------------------------------------------------
    # Limites básicos
    # --------------------------------------------------------

    if len(text) > 120:
        return False

    words = text.split()

    if len(words) > 15:
        return False

    # --------------------------------------------------------
    # Não considerar números isolados como heading
    # --------------------------------------------------------

    if text.isdigit():
        return False

    # --------------------------------------------------------
    # Artigos não são headings
    # --------------------------------------------------------

    if re.match(
        r"^Art\.\s*\d+",
        text,
        re.IGNORECASE,
    ):
        return False

    # --------------------------------------------------------
    # Não considerar frases terminadas em pontuação
    # --------------------------------------------------------

    if text.endswith(
        (".", ";", ":", ",")
    ):
        return False

    # --------------------------------------------------------
    # 1. Heading totalmente em maiúsculas
    # --------------------------------------------------------

    letters = [
        char
        for char in text
        if char.isalpha()
    ]

    if letters:

        uppercase_ratio = (
            sum(
                char.isupper()
                for char in letters
            )
            / len(letters)
        )

        if uppercase_ratio >= 0.70:
            return True

    # --------------------------------------------------------
    # 2. Subtítulos em Title Case
    #
    # Exemplo:
    #     Das Imunidades
    #     Princípios Constitucionais
    #     Regimes Diferenciados
    # --------------------------------------------------------

    title_case_words = 0

    for word in words:

        clean_word = re.sub(
            r"^[^A-Za-zÁÀÂÃÉÊÍÓÔÕÚÇáàâãéêíóôõúç]+|"
            r"[^A-Za-zÁÀÂÃÉÊÍÓÔÕÚÇáàâãéêíóôõúç]+$",
            "",
            word,
        )

        if not clean_word:
            continue

        # Primeira letra maiúscula
        # restante predominantemente minúsculo
        if (
            clean_word[0].isupper()
            and clean_word[1:].islower()
        ):
            title_case_words += 1

    if words:

        title_case_ratio = (
            title_case_words
            / len(words)
        )

        # Evita classificar frases normais como heading.
        #
        # Para títulos curtos, 50% é suficiente.
        if (
            len(words) <= 5
            and title_case_ratio >= 0.50
        ):
            return True

    return False

def is_list_item(text: str) -> bool:
    """
    Identifica itens de listas.

    Exemplos reconhecidos:

        • item

        - item

        * item

        1. item

        2) item
    """

    return bool(
        re.match(
            r"^(?:•|-|\*|\d+[.)])\s+",
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

    Apenas recebe a sinalização:

        numeric_heavy
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


def is_module_heading(text: str) -> bool:
    """
    Identifica títulos de módulo.

    Exemplos reconhecidos:

        Módulo 1
        Módulo 1 - Reforma Tributária
        Módulo 2 — IBS e CBS
        MODULO 3
        MÓDULO 4

    A identificação é baseada no padrão textual
    "Módulo" seguido de um número.
    """

    text = text.strip()

    if not text:
        return False

    pattern = r"^(?:módulo|modulo)\s+\d+(?:\s*[-–—:]\s*.+)?$"

    return bool(
        re.match(
            pattern,
            text,
            flags=re.IGNORECASE,
        )
    )

def infer_module_from_document(
    document_metadata: dict[str, Any],
) -> str | None:
    """
    Infere o módulo a partir dos metadados do documento.

    Exemplos:

        Modulo_1_parte_1.pdf
            -> Módulo 1

        Modulo_2.pdf
            -> Módulo 2

        Modulo_3_parte_2.pdf
            -> Módulo 3

    Caso o documento não siga esse padrão, retorna None.
    """

    document_name = document_metadata.get(
        "document_name",
        "",
    )

    if not document_name:
        return None

    match = re.search(
        r"(?:módulo|modulo)[_\s-]*(\d+)",
        document_name,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    module_number = match.group(1)

    return f"Módulo {module_number}"

# ============================================================
# CONTEXTO ESTRUTURAL
# ============================================================

def infer_heading_context(
    paragraphs: list[str],
) -> list[dict[str, str | None]]:
    """
    Identifica e mantém o contexto estrutural do documento.

    Hierarquia:

        Módulo
            ↓
        Seção
            ↓
        Tópico
            ↓
        Conteúdo

    Estratégia:

        Módulo
            → module

        Primeiro heading após o módulo
            → section

        Próximos headings
            → topic

    O texto original não é alterado.

    Returns
    -------
    list[dict[str, str | None]]
        Cada item contém:

            text
            module
            section
            topic
    """

    contextualized: list[
        dict[str, str | None]
    ] = []

    current_module: str | None = None
    current_section: str | None = None
    current_topic: str | None = None

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        # ====================================================
        # MÓDULO
        # ====================================================

        if is_module_heading(paragraph):

            current_module = paragraph
            current_section = None
            current_topic = None

            contextualized.append(
                {
                    "text": paragraph,
                    "module": current_module,
                    "section": None,
                    "topic": None,
                }
            )

            continue

        # ====================================================
        # OUTROS HEADINGS
        # ====================================================

        if is_heading(paragraph):

            # ------------------------------------------------
            # Primeiro heading após o módulo = seção
            # ------------------------------------------------

            if current_section is None:

                current_section = paragraph
                current_topic = None

            # ------------------------------------------------
            # Próximos headings = tópicos
            # ------------------------------------------------

            else:

                current_topic = paragraph

            contextualized.append(
                {
                    "text": paragraph,
                    "module": current_module,
                    "section": current_section,
                    "topic": current_topic,
                }
            )

            continue

        # ====================================================
        # CONTEÚDO NORMAL
        # ====================================================

        contextualized.append(
            {
                "text": paragraph,
                "module": current_module,
                "section": current_section,
                "topic": current_topic,
            }
        )

    return contextualized

# ============================================================
# QUALIDADE
# ============================================================

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
    module: str | None = None,
    section: str | None = None,
    topic: str | None = None,
) -> dict[str, Any]:
    """
    Cria um chunk padronizado com conteúdo,
    metadados documentais e indicadores de qualidade.
    """

    text = text.strip()

    flags: list[str] = []

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

        # ----------------------------------------------------
        # Identificação documental
        # ----------------------------------------------------

        "document_id": document_metadata["document_id"],
        "document_name": document_metadata["document_name"],
        "document_type": document_metadata["document_type"],
        "source_organization": document_metadata[
            "source_organization"
        ],
        "publication_date": document_metadata.get(
            "publication_date"
        ),
        "source_url": document_metadata.get(
            "source_url"
        ),

        # ----------------------------------------------------
        # Localização e contexto
        # ----------------------------------------------------

        "page": page,
        "module": module,
        "section": section,
        "topic": topic,

        # ----------------------------------------------------
        # Controle do chunk
        # ----------------------------------------------------

        "chunk_index": chunk_index,

        # ----------------------------------------------------
        # Conteúdo
        # ----------------------------------------------------

        "text": text,
        "char_count": len(text),

        # ----------------------------------------------------
        # Qualidade
        # ----------------------------------------------------

        "quality_score": calculate_quality_score(
            text
        ),
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
        contexto estrutural
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

    document_metadata:
        Metadados do documento.

    chunk_size:
        Tamanho aproximado do chunk.

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
    # 3. METADADOS / CONTEXTO EXISTENTE
    # ========================================================

    module = (
    page.get("module")
    or document_metadata.get("module")
    or infer_module_from_document(
        document_metadata
    )
)

    existing_section = page.get(
        "section"
    )

    existing_topic = page.get(
        "topic"
    )

    # ========================================================
    # 4. PARÁGRAFOS
    # ========================================================

    paragraphs = split_into_paragraphs(
        text
    )

    if not paragraphs:
        return []

    # ========================================================
    # 5. INFERÊNCIA DE CONTEXTO
    # ========================================================

    contextualized_paragraphs = (
        infer_heading_context(
            paragraphs
        )
    )

    # ========================================================
    # 6. AGRUPAMENTO
    # ========================================================

    chunks: list[dict[str, Any]] = []

    current_parts: list[str] = []
    current_length = 0

    current_section = existing_section
    current_topic = existing_topic

    for item in contextualized_paragraphs:

        paragraph = item["text"]

        inferred_module = item["module"]
        inferred_section = item["section"]
        inferred_topic = item["topic"]

        if inferred_module is not None:
            module = inferred_module

        if inferred_section is not None:
            current_section = inferred_section

        if inferred_topic is not None:
            current_topic = inferred_topic

        paragraph_length = len(paragraph)
        # ====================================================
        # PARÁGRAFO MUITO GRANDE
        # ====================================================

        if paragraph_length > chunk_size:

            # ------------------------------------------------
            # Finaliza conteúdo acumulado
            # ------------------------------------------------

            if current_parts:

                chunks.append(
                    {
                        "text": "\n\n".join(
                            current_parts
                        ),
                        "section": current_section,
                        "topic": current_topic,
                    }
                )

                current_parts = []
                current_length = 0

            # ------------------------------------------------
            # Divide parágrafo grande
            # ------------------------------------------------

            large_chunks = split_text(
                paragraph,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            for large_chunk in large_chunks:

                chunks.append(
                    {
                        "text": large_chunk,
                        "section": current_section,
                        "topic": current_topic,
                    }
                )

            continue

        # ====================================================
        # TÍTULO
        # ====================================================

        if is_heading(paragraph):

            if current_parts:

                chunks.append(
                    {
                        "text": "\n\n".join(
                            current_parts
                        ),
                        "section": current_section,
                        "topic": current_topic,
                    }
                )

                current_parts = []
                current_length = 0

            current_parts.append(
                paragraph
            )

            current_length = paragraph_length

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
                    {
                        "text": "\n\n".join(
                            current_parts
                        ),
                        "section": current_section,
                        "topic": current_topic,
                    }
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
                {
                    "text": "\n\n".join(
                        current_parts
                    ),
                    "section": current_section,
                    "topic": current_topic,
                }
            )

            # ------------------------------------------------
            # OVERLAP
            # ------------------------------------------------

            overlap_parts: list[str] = []
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
    # 7. ÚLTIMO CHUNK
    # ========================================================

    if current_parts:

        chunks.append(
            {
                "text": "\n\n".join(
                    current_parts
                ),
                "section": current_section,
                "topic": current_topic,
            }
        )

    # ========================================================
    # 8. CRIAÇÃO DOS OBJETOS
    # ========================================================

    result: list[dict[str, Any]] = []

    for index, chunk_data in enumerate(
        chunks
    ):

        result.append(
            create_chunk(
                text=chunk_data["text"],
                page=page_number,
                chunk_index=index,
                document_metadata=document_metadata,
                module=module,
                section=chunk_data["section"],
                topic=chunk_data["topic"],
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
    """
    Processa todas as páginas de um documento.

    O índice dos chunks é global para todo o documento.

    Returns
    -------
    list[dict[str, Any]]
        Lista completa de chunks.
    """

    # --------------------------------------------------------
    # Validação dos metadados
    # --------------------------------------------------------

    validate_document_metadata(
        document_metadata
    )

    # --------------------------------------------------------
    # Validação do documento
    # --------------------------------------------------------

    if not isinstance(document, list):
        raise TypeError(
            "document deve ser uma lista."
        )

    # --------------------------------------------------------
    # Validação do chunking
    # --------------------------------------------------------

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

    chunks: list[dict[str, Any]] = []

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

            chunk["chunk_index"] = (
                global_index
            )

            chunks.append(chunk)

    return chunks
