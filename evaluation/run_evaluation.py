"""
Executa a avaliação real da recuperação semântica.

Fluxo:

evaluation_questions.json
        ↓
RAG real
        ↓
Retriever real
        ↓
Vector Store real
        ↓
Métricas de recuperação
"""

import sys
import json
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS DO PROJETO
# ============================================================

from app.rag import create_rag

from evaluation.evaluate_retrieval import (
    evaluate_retrieval,
)


# ============================================================
# ARQUIVO DE PERGUNTAS
# ============================================================

QUESTIONS_FILE = (
    BASE_DIR / "evaluation_questions.json"
)

def main() -> None:

    # --------------------------------------------------------
    # 1. Carregar perguntas
    # --------------------------------------------------------

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        questions = json.load(file)

    if not isinstance(questions, list):
        raise TypeError(
            "evaluation_questions.json deve "
            "conter uma lista."
        )

    # --------------------------------------------------------
    # 2. Criar RAG real
    # --------------------------------------------------------

    rag = create_rag()

    # --------------------------------------------------------
    # 3. Executar avaliação
    # --------------------------------------------------------

    result = evaluate_retrieval(
        rag=rag,
        questions=questions,
        k=5,
    )

    # --------------------------------------------------------
    # 4. Exibir resultados
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("📊 AVALIAÇÃO REAL DO RETRIEVER")
    print("=" * 60)

    print(
        f"Perguntas avaliadas: "
        f"{result['total_questions']}"
    )

    print(
        f"Top-K: "
        f"{result['k']}"
    )

    print(
        f"Hit@K: "
        f"{result['hit_at_k']:.2%}"
    )

    print(
        f"Document Hit Rate: "
        f"{result['document_hit_rate']:.2%}"
    )

    print(
        f"Source Hit Rate: "
        f"{result['source_hit_rate']:.2%}"
    )

    print(
        f"Page Hit Rate: "
        f"{result['page_hit_rate']:.2%}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # 5. Detalhamento
    # --------------------------------------------------------

    print()
    print("📋 DETALHAMENTO")
    print("-" * 60)

    for item in result.get(
        "questions",
        [],
    ):

        print(
            f"{item['id']} | "
            f"Hit: {item['hit']} | "
            f"Documento: {item['document_hit']} | "
            f"Fonte: {item['source_hit']} | "
            f"Página: {item['page_hit']} | "
            f"Rank: {item['rank']}"
        )


if __name__ == "__main__":
    main()