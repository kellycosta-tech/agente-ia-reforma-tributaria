"""
Avaliação real da recuperação do RAG.

Responsabilidades:

    1. Carregar perguntas de avaliação.
    2. Executar as perguntas no RAG.
    3. Verificar documento esperado.
    4. Verificar organização/fonte esperada.
    5. Verificar página esperada.
    6. Calcular Hit@K.
    7. Calcular MRR.
    8. Gerar relatório detalhado.

Nesta etapa avaliamos a recuperação.

A avaliação da resposta gerada pelo LLM será realizada
posteriormente.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.rag import RAG, create_rag


# ============================================================
# CONFIGURAÇÃO
# ============================================================

DEFAULT_QUESTIONS_PATH = (
    Path(__file__).resolve().parent
    / "evaluation_questions.json"
)


# ============================================================
# NORMALIZAÇÃO
# ============================================================

def normalize_text(
    value: Any,
) -> str:
    """
    Normaliza texto para comparação.
    """

    if not isinstance(value, str):
        return ""

    return value.strip().lower()


# ============================================================
# CARREGAMENTO
# ============================================================

def load_evaluation_questions(
    path: str | Path = DEFAULT_QUESTIONS_PATH,
) -> list[dict[str, Any]]:
    """
    Carrega as perguntas de avaliação.

    Formato esperado:

    {
        "id": "q001",
        "question": "...",
        "answer": "...",
        "expected_document": "...",
        "expected_source": "...",
        "expected_pages": [1]
    }
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo de avaliação não encontrado: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise TypeError(
            "O arquivo de avaliação deve conter uma lista."
        )

    for item in data:

        if not isinstance(item, dict):
            raise TypeError(
                "Cada avaliação deve ser um dicionário."
            )

        if "id" not in item:
            raise ValueError(
                "Cada avaliação deve possuir 'id'."
            )

        if "question" not in item:
            raise ValueError(
                "Cada avaliação deve possuir 'question'."
            )

        if "expected_document" not in item:
            raise ValueError(
                "Cada avaliação deve possuir "
                "'expected_document'."
            )

        if "expected_source" not in item:
            raise ValueError(
                "Cada avaliação deve possuir "
                "'expected_source'."
            )

        if "expected_pages" not in item:
            raise ValueError(
                "Cada avaliação deve possuir "
                "'expected_pages'."
            )

        if not isinstance(
            item["expected_pages"],
            list,
        ):
            raise TypeError(
                "'expected_pages' deve ser uma lista."
            )

    return data


# ============================================================
# AVALIAÇÃO INDIVIDUAL
# ============================================================

def evaluate_question(
    rag: RAG,
    question: dict[str, Any],
    k: int = 5,
) -> dict[str, Any]:
    """
    Avalia uma pergunta individual.

    Verifica:

        - documento;
        - fonte;
        - página;
        - posição do documento esperado.

    Calcula:

        - Hit@K;
        - Reciprocal Rank.
    """

    if not isinstance(
        question,
        dict,
    ):
        raise TypeError(
            "question deve ser um dicionário."
        )

    query = question.get(
        "question"
    )

    if not isinstance(
        query,
        str,
    ):
        raise TypeError(
            "'question' deve ser uma string."
        )

    query = query.strip()

    if not query:
        raise ValueError(
            "A pergunta não pode estar vazia."
        )

    if not isinstance(
        k,
        int,
    ):
        raise TypeError(
            "k deve ser um inteiro."
        )

    if k <= 0:
        raise ValueError(
            "k deve ser maior que zero."
        )

    expected_document = normalize_text(
        question.get(
            "expected_document"
        )
    )

    expected_source = normalize_text(
        question.get(
            "expected_source"
        )
    )

    expected_pages = set(
        question.get(
            "expected_pages",
            []
        )
    )

    results = rag.retrieve(
        query=query,
        k=k,
    )

    retrieved_documents = []
    retrieved_sources = []
    retrieved_pages = []

    document_rank = None
    source_rank = None
    page_rank = None

    for rank, result in enumerate(
        results,
        start=1,
    ):

        if not isinstance(
            result,
            dict,
        ):
            continue

        document = normalize_text(
            result.get(
                "document_name"
            )
        )

        source = normalize_text(
            result.get(
                "source_organization"
            )
        )

        page = result.get(
            "page"
        )

        retrieved_documents.append(
            result.get(
                "document_name"
            )
        )

        retrieved_sources.append(
            result.get(
                "source_organization"
            )
        )

        retrieved_pages.append(
            page
        )

        if (
            document_rank is None
            and document == expected_document
        ):
            document_rank = rank

        if (
            source_rank is None
            and source == expected_source
        ):
            source_rank = rank

        if (
            page_rank is None
            and page in expected_pages
        ):
            page_rank = rank

    # --------------------------------------------------------
    # MÉTRICAS
    # --------------------------------------------------------

    document_hit = (
        document_rank is not None
    )

    source_hit = (
        source_rank is not None
    )

    page_hit = document_hit and any(
    page in expected_pages
    for page in retrieved_pages
)

    # Hit principal:
    # documento + fonte + página
    hit_at_k = (
        document_hit
        and source_hit
        and page_hit
    )

    # Para MRR utilizamos o primeiro ranking
    # em que o documento esperado aparece.
    reciprocal_rank = 0.0

    if document_rank is not None:
        reciprocal_rank = (
            1.0 / document_rank
        )

    return {
        "id": question.get("id"),
        "question": query,
        "expected_document": question.get(
            "expected_document"
        ),
        "expected_source": question.get(
            "expected_source"
        ),
        "expected_pages": question.get(
            "expected_pages"
        ),
        "retrieved_documents": retrieved_documents,
        "retrieved_sources": retrieved_sources,
        "retrieved_pages": retrieved_pages,
        "document_hit": document_hit,
        "source_hit": source_hit,
        "page_hit": page_hit,
        "hit_at_k": hit_at_k,
        "document_rank": document_rank,
        "source_rank": source_rank,
        "page_rank": page_rank,
        "reciprocal_rank": reciprocal_rank,
    }


# ============================================================
# AVALIAÇÃO COMPLETA
# ============================================================

def evaluate_retrieval(
    rag: RAG,
    questions: list[dict[str, Any]],
    k: int = 5,
) -> dict[str, Any]:
    """
    Executa a avaliação completa da recuperação.
    """

    if not isinstance(
        questions,
        list,
    ):
        raise TypeError(
            "questions deve ser uma lista."
        )

    if not questions:
        raise ValueError(
            "A lista de perguntas não pode estar vazia."
        )

    results = []

    for question in questions:

        result = evaluate_question(
            rag=rag,
            question=question,
            k=k,
        )

        results.append(
            result
        )

    total = len(results)

    document_hits = sum(
        result["document_hit"]
        for result in results
    )

    source_hits = sum(
        result["source_hit"]
        for result in results
    )

    page_hits = sum(
        result["page_hit"]
        for result in results
    )

    hits = sum(
        result["hit_at_k"]
        for result in results
    )

    hit_at_k = (
        hits / total
    )

    document_hit_rate = (
        document_hits / total
    )

    source_hit_rate = (
        source_hits / total
    )

    page_hit_rate = (
        page_hits / total
    )

    mrr = sum(
        result["reciprocal_rank"]
        for result in results
    ) / total

    return {
        "total_questions": total,
        "k": k,
        "hit_at_k": hit_at_k,
        "document_hit_rate": document_hit_rate,
        "source_hit_rate": source_hit_rate,
        "page_hit_rate": page_hit_rate,
        "mrr": mrr,
        "results": results,
    }


# ============================================================
# RELATÓRIO
# ============================================================

def print_report(
    evaluation: dict[str, Any],
) -> None:
    """
    Exibe o relatório da avaliação.
    """

    k = evaluation["k"]

    print()
    print("=" * 72)
    print("AVALIAÇÃO REAL DA RECUPERAÇÃO DO RAG")
    print("=" * 72)

    print(
        f"Perguntas avaliadas : "
        f"{evaluation['total_questions']}"
    )

    print(
        f"K                    : "
        f"{k}"
    )

    print(
        f"Hit@{k}               : "
        f"{evaluation['hit_at_k']:.2%}"
    )

    print(
        f"Documento correto     : "
        f"{evaluation['document_hit_rate']:.2%}"
    )

    print(
        f"Fonte correta         : "
        f"{evaluation['source_hit_rate']:.2%}"
    )

    print(
        f"Página correta        : "
        f"{evaluation['page_hit_rate']:.2%}"
    )

    print(
        f"MRR                   : "
        f"{evaluation['mrr']:.4f}"
    )

    print()
    print("-" * 72)
    print("RESULTADOS INDIVIDUAIS")
    print("-" * 72)

    for result in evaluation["results"]:

        status = (
            "✅"
            if result["hit_at_k"]
            else "❌"
        )

        print()
        print(
            f"{status} {result['id']} "
            f"- {result['question']}"
        )

        print(
            "   Documento esperado: "
            f"{result['expected_document']}"
        )

        print(
            "   Documentos recuperados: "
            f"{result['retrieved_documents']}"
        )

        print(
            "   Fonte esperada: "
            f"{result['expected_source']}"
        )

        print(
            "   Fontes recuperadas: "
            f"{result['retrieved_sources']}"
        )

        print(
            "   Páginas esperadas: "
            f"{result['expected_pages']}"
        )

        print(
            "   Páginas recuperadas: "
            f"{result['retrieved_pages']}"
        )

        print(
            "   Rank documento: "
            f"{result['document_rank']}"
        )

        print(
            "   Rank página: "
            f"{result['page_rank']}"
        )

    print()
    print("=" * 72)


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """
    Executa a avaliação real.
    """

    questions = load_evaluation_questions()

    rag = create_rag()

    evaluation = evaluate_retrieval(
        rag=rag,
        questions=questions,
        k=5,
    )

    print_report(
        evaluation
    )


if __name__ == "__main__":
    main()