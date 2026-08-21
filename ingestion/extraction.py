"""
Extraction
==========

Responsabilidade:
    Receber o conteúdo extraído pelos loaders e
    padronizar sua estrutura para as próximas etapas
    do pipeline RAG.

Este módulo NÃO é responsável por:

    - abrir arquivos PDF;
    - limpar texto;
    - criar chunks;
    - gerar embeddings;
    - armazenar vetores;
    - realizar consultas no RAG.

Arquitetura:

    Documento
        ↓
    Loader específico
        ↓
    Extraction
        ↓
    Cleaning
        ↓
    Chunking
        ↓
    Metadata
        ↓
    Embeddings
        ↓
    Vector Store
"""

from pathlib import Path
from typing import Any

from ingestion.loaders.pdf_loader import load_pdf


def extract_document(
    file_path: str | Path,
) -> list[dict[str, Any]]:
    """
    Extrai e padroniza o conteúdo de um documento.

    Atualmente, o projeto suporta a extração de PDF.

    Parameters
    ----------
    file_path : str | Path
        Caminho do documento que será processado.

    Returns
    -------
    list[dict[str, Any]]
        Conteúdo estruturado do documento.

    Exemplo:

        [
            {
                "page": 1,
                "text": "Conteúdo da página 1"
            },
            {
                "page": 2,
                "text": "Conteúdo da página 2"
            }
        ]

    Raises
    ------
    FileNotFoundError
        Se o documento não existir.

    ValueError
        Se o formato não for suportado.

    NotImplementedError
        Se o formato for previsto na arquitetura,
        mas ainda não tiver um loader implementado.
    """

    # ---------------------------------------------------------
    # 1. Normalização do caminho
    # ---------------------------------------------------------

    file_path = Path(file_path)

    # ---------------------------------------------------------
    # 2. Validação da existência do arquivo
    # ---------------------------------------------------------

    if not file_path.exists():
        raise FileNotFoundError(
            f"Documento não encontrado: {file_path}"
        )

    # ---------------------------------------------------------
    # 3. Identificação do formato
    # ---------------------------------------------------------

    extension = file_path.suffix.lower()

    # ---------------------------------------------------------
    # 4. PDF
    # ---------------------------------------------------------

    if extension == ".pdf":

        return load_pdf(file_path)

    # ---------------------------------------------------------
    # 5. Formatos planejados
    # ---------------------------------------------------------

    supported_formats = {
        ".pdf",
        ".docx",
        ".xlsx",
        ".pptx",
        ".md",
        ".csv",
        ".json",
        ".html",
    }

    # ---------------------------------------------------------
    # 6. Formato conhecido, mas ainda não implementado
    # ---------------------------------------------------------

    if extension in supported_formats:

        raise NotImplementedError(
            f"O formato '{extension}' está previsto "
            "na arquitetura, mas ainda não possui "
            "um loader implementado."
        )

    # ---------------------------------------------------------
    # 7. Formato desconhecido
    # ---------------------------------------------------------

    raise ValueError(
        f"Formato de arquivo não suportado: {extension}"
    )