"""
Prompts utilizados pelo agente de RAG.

Responsabilidades:

    1. Definir as instruções do sistema.
    2. Construir o prompt com a pergunta do usuário.
    3. Inserir o contexto recuperado pelo RAG.
    4. Orientar o LLM a responder somente com base nas fontes.
    5. Preservar a rastreabilidade das informações.

Fluxo:

    Pergunta
       ↓
    Retriever
       ↓
    Contexto
       ↓
    Prompt
       ↓
    LLM
       ↓
    Resposta fundamentada
"""

from __future__ import annotations


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
Você é um assistente especializado em Reforma Tributária do Consumo.

Sua função é responder perguntas utilizando exclusivamente as
informações presentes no contexto documental fornecido.

Regras:

1. Responda em português do Brasil.
2. Utilize somente informações presentes no contexto.
3. Não invente informações, leis, artigos, datas ou interpretações.
4. Quando o contexto não for suficiente para responder, informe
   claramente que não foram encontradas evidências suficientes
   na base documental.
5. Priorize precisão e clareza.
6. Sempre que possível, informe a fonte utilizada.
7. Preserve a rastreabilidade indicando documento e página quando
   essas informações estiverem disponíveis.
8. Não apresente conhecimento externo ao contexto como se fosse
   proveniente dos documentos recuperados.
9. Quando houver informações conflitantes no contexto, sinalize
   a divergência em vez de escolher uma informação sem justificativa.
10. Não crie citações ou páginas que não estejam presentes nos dados
    recuperados.
""".strip()


# ============================================================
# PROMPT TEMPLATE
# ============================================================

USER_PROMPT_TEMPLATE = """
Pergunta do usuário:

{query}

Contexto documental recuperado:

{context}

Instruções para resposta:

- Responda diretamente à pergunta.
- Baseie a resposta exclusivamente no contexto fornecido.
- Seja claro, objetivo e tecnicamente preciso.
- Ao utilizar uma informação do contexto, informe a fonte
  correspondente.
- Quando disponível, informe documento e página.
- Se o contexto não contiver informações suficientes, diga
  explicitamente que não há evidências suficientes na base
  documental para responder com segurança.

Resposta:
""".strip()


# ============================================================
# BUILD PROMPT
# ============================================================

def build_prompt(
    query: str,
    context: str,
) -> str:
    """
    Constrói o prompt enviado ao modelo de linguagem.

    Parameters
    ----------
    query:
        Pergunta realizada pelo usuário.

    context:
        Contexto recuperado pelo RAG.

    Returns
    -------
    str
        Prompt formatado para o LLM.
    """

    if not isinstance(query, str):
        raise TypeError(
            "query deve ser uma string."
        )

    if not isinstance(context, str):
        raise TypeError(
            "context deve ser uma string."
        )

    query = query.strip()
    context = context.strip()

    if not query:
        raise ValueError(
            "query não pode estar vazia."
        )

    if not context:
        raise ValueError(
            "context não pode estar vazio."
        )

    return USER_PROMPT_TEMPLATE.format(
        query=query,
        context=context,
    )


# ============================================================
# BUILD MESSAGES
# ============================================================

def build_messages(
    query: str,
    context: str,
) -> list[dict[str, str]]:
    """
    Constrói as mensagens no formato utilizado por LLMs.

    Returns
    -------
    list[dict[str, str]]
        Lista contendo mensagem de sistema e mensagem do usuário.
    """

    prompt = build_prompt(
        query=query,
        context=context,
    )

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]