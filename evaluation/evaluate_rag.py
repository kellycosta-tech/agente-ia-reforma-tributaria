"""
Avaliação do pipeline RAG.

Este script executa perguntas reais contra o Agent
e avalia:

- presença de resposta;
- recuperação das fontes esperadas;
- recuperação das páginas esperadas;
- presença dos tópicos esperados;
- respostas sem evidência;
- qualidade básica da resposta.

IMPORTANTE:
Este arquivo NÃO faz parte dos testes unitários.

Ele utiliza o LLM configurado no ambiente.
"""

"""
Avaliação do pipeline RAG.
"""

from pathlib import Path
import sys
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agent import create_agent

# ============================================================
# CONFIGURAÇÃO
# ============================================================

QUESTIONS_FILE = (
    Path(__file__).parent / "questions.json"
)


# ============================================================
# CARREGAMENTO
# ============================================================

def load_questions() -> list[dict]:
    """
    Carrega as perguntas do dataset de avaliação.
    """

    if not QUESTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {QUESTIONS_FILE}"
        )

    with QUESTIONS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        questions = json.load(file)

    if not isinstance(questions, list):
        raise ValueError(
            "questions.json deve conter uma lista."
        )

    return questions


# ============================================================
# AVALIAÇÃO DE FONTES
# ============================================================

def evaluate_document(
    result: dict,
    expected_document: str | None,
) -> bool:
    """
    Verifica se o documento esperado foi recuperado.
    """

    if expected_document is None:
        return True

    sources = result.get("sources", [])

    return any(
        source.get("document_name")
        == expected_document
        for source in sources
    )


def evaluate_source(
    result: dict,
    expected_source: str | None,
) -> bool:
    """
    Verifica se a organização esperada foi recuperada.
    """

    if expected_source is None:
        return True

    sources = result.get("sources", [])

    return any(
        source.get("source_organization")
        == expected_source
        for source in sources
    )


def evaluate_pages(
    result: dict,
    expected_pages: list[int],
) -> bool:
    """
    Verifica se pelo menos uma das páginas esperadas
    foi recuperada.
    """

    if not expected_pages:
        return True

    retrieved_pages = {
        source.get("page")
        for source in result.get("sources", [])
    }

    return bool(
        retrieved_pages.intersection(
            expected_pages
        )
    )


# ============================================================
# AVALIAÇÃO DE TÓPICOS
# ============================================================

def evaluate_topics(
    answer: str,
    expected_topics: list[str],
) -> tuple[int, int]:
    """
    Verifica quantos tópicos esperados aparecem
    na resposta.

    Retorna:

        (tópicos encontrados, total de tópicos)
    """

    if not expected_topics:
        return 0, 0

    normalized_answer = answer.lower()

    found = 0

    for topic in expected_topics:

        if topic.lower() in normalized_answer:
            found += 1

    return found, len(expected_topics)


# ============================================================
# AVALIAÇÃO DE RESPOSTA
# ============================================================

def evaluate_answer(
    result: dict,
) -> bool:
    """
    Verifica se o agente produziu uma resposta válida.
    """

    answer = result.get("answer")

    return (
        isinstance(answer, str)
        and bool(answer.strip())
    )


# ============================================================
# EXECUÇÃO
# ============================================================

def evaluate_question(
    agent,
    question_data: dict,
) -> dict:
    """
    Executa uma pergunta e retorna os indicadores
    da avaliação.
    """

    question = question_data["question"]

    result = agent.ask(question)

    answer = result.get(
        "answer",
        "",
    )

    expected_document = question_data.get(
        "expected_document"
    )

    expected_source = question_data.get(
        "expected_source"
    )

    expected_pages = question_data.get(
        "expected_pages",
        [],
    )

    expected_topics = question_data.get(
        "expected_topics",
        [],
    )

    answer_ok = evaluate_answer(
        result
    )

    document_ok = evaluate_document(
        result,
        expected_document,
    )

    source_ok = evaluate_source(
        result,
        expected_source,
    )

    pages_ok = evaluate_pages(
        result,
        expected_pages,
    )

    topics_found, topics_total = (
        evaluate_topics(
            answer,
            expected_topics,
        )
    )

    if topics_total > 0:

        topic_score = (
            topics_found / topics_total
        )

    else:

        topic_score = 1.0

    return {
        "id": question_data["id"],
        "category": question_data.get(
            "category",
            "unknown",
        ),
        "question": question,
        "answer": answer,
        "sources": result.get(
            "sources",
            [],
        ),
        "answer_ok": answer_ok,
        "document_ok": document_ok,
        "source_ok": source_ok,
        "pages_ok": pages_ok,
        "topics_found": topics_found,
        "topics_total": topics_total,
        "topic_score": topic_score,
    }


# ============================================================
# TABELA
# ============================================================

def print_results(
    results: list[dict],
) -> None:
    """
    Exibe uma tabela resumida da avaliação.
    """

    print()
    print("=" * 100)
    print("📊 AVALIAÇÃO DO RAG")
    print("=" * 100)

    header = (
        f"{'ID':<8}"
        f"{'Categoria':<15}"
        f"{'Resposta':<12}"
        f"{'Documento':<12}"
        f"{'Fonte':<10}"
        f"{'Página':<10}"
        f"{'Tópicos':<10}"
    )

    print(header)
    print("-" * 100)

    for item in results:

        topics = (
            f"{item['topics_found']}/"
            f"{item['topics_total']}"
        )

        print(
            f"{item['id']:<8}"
            f"{item['category']:<15}"
            f"{'✅' if item['answer_ok'] else '❌':<12}"
            f"{'✅' if item['document_ok'] else '❌':<12}"
            f"{'✅' if item['source_ok'] else '❌':<10}"
            f"{'✅' if item['pages_ok'] else '❌':<10}"
            f"{topics:<10}"
        )

    print("=" * 100)


# ============================================================
# RESUMO
# ============================================================

def print_summary(
    results: list[dict],
) -> None:
    """
    Exibe métricas consolidadas.
    """

    total = len(results)

    if total == 0:
        return

    answers = sum(
        item["answer_ok"]
        for item in results
    )

    documents = sum(
        item["document_ok"]
        for item in results
    )

    sources = sum(
        item["source_ok"]
        for item in results
    )

    pages = sum(
        item["pages_ok"]
        for item in results
    )

    topic_scores = [
        item["topic_score"]
        for item in results
    ]

    average_topics = (
        sum(topic_scores)
        / len(topic_scores)
    )

    print()
    print("📈 RESUMO")
    print("-" * 50)

    print(
        f"Perguntas avaliadas: {total}"
    )

    print(
        f"Respostas válidas: "
        f"{answers}/{total} "
        f"({answers / total:.1%})"
    )

    print(
        f"Documento esperado recuperado: "
        f"{documents}/{total} "
        f"({documents / total:.1%})"
    )

    print(
        f"Fonte esperada recuperada: "
        f"{sources}/{total} "
        f"({sources / total:.1%})"
    )

    print(
        f"Página esperada recuperada: "
        f"{pages}/{total} "
        f"({pages / total:.1%})"
    )

    print(
        f"Cobertura média dos tópicos: "
        f"{average_topics:.1%}"
    )


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print(
        "🚀 Iniciando avaliação do pipeline RAG..."
    )

    questions = load_questions()

    print(
        f"📋 Perguntas carregadas: "
        f"{len(questions)}"
    )

    print(
        "🤖 Criando Agent..."
    )

    agent = create_agent()

    results = []

    for index, question_data in enumerate(
        questions,
        start=1,
    ):

        print()
        print(
            f"🔎 Avaliando "
            f"{index}/{len(questions)}: "
            f"{question_data['id']}"
        )

        try:

            evaluation = evaluate_question(
                agent,
                question_data,
            )

            results.append(
                evaluation
            )

        except Exception as error:

            print(
                f"❌ Erro: {error}"
            )

    print_results(results)

    print_summary(results)


if __name__ == "__main__":
    main()