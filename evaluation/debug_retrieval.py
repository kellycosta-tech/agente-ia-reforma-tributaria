"""
Diagnóstico da recuperação semântica real.

Mostra os Top-K resultados recuperados pelo RAG
para as perguntas da avaliação.
"""

from pathlib import Path
import sys


# ============================================================
# CONFIGURAÇÃO DO PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from app.rag import create_rag


# ============================================================
# PERGUNTAS
# ============================================================

QUESTIONS = [
    "O que é a Reforma Tributária do Consumo?",
    "Quais são os princípios constitucionais da Reforma Tributária do Consumo?",
    "Como funcionará o mecanismo de cashback para famílias de baixa renda?",
    "Quais operações são imunes ao IBS e à CBS segundo a Lei Complementar 214?",
    "Como será feita a distribuição da receita do IBS entre Estados e Municípios durante a transição?",
]


# ============================================================
# DIAGNÓSTICO
# ============================================================

def main() -> None:

    rag = create_rag()

    print("=" * 70)
    print("🔎 DIAGNÓSTICO DA RECUPERAÇÃO SEMÂNTICA + RERANKING")
    print("=" * 70)

    for number, question in enumerate(QUESTIONS, start=1):

        print()
        print("=" * 70)
        print(f"PERGUNTA {number}")
        print("=" * 70)

        print(f"\nPergunta:")
        print(question)

        results = rag.retrieve(
            query=question,
            k=5,
        )

        print()
        print(f"Resultados recuperados: {len(results)}")
        print("-" * 70)

        if not results:
            print("❌ Nenhum resultado recuperado.")
            continue

        for rank, result in enumerate(results, start=1):

            print()
            print(f"#{rank}")

            print(
                f"Documento: "
                f"{result.get('document_name')}"
            )

            print(
                f"Organização: "
                f"{result.get('source_organization')}"
            )

            print(
                f"Módulo: "
                f"{result.get('module')}"
            )

            print(
                f"Página: "
                f"{result.get('page')}"
            )

            print(
                f"Seção: "
                f"{result.get('section')}"
            )

            print(
    f"Similaridade: "
    f"{result.get('similarity')}"
)

            print(
                f"Rerank Score: "
                f"{result.get('rerank_score')}"
            )

            text = result.get("text", "")

            print("Texto:")

            print(text[:500])

            print("-" * 70)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()