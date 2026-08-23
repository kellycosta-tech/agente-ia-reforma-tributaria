"""
Testes da camada de prompts.

Valida:

    prompts.py
        ↓
    construção do prompt
        ↓
    construção das mensagens para o LLM
"""


import pytest

from app.prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    build_messages,
    build_prompt,
)


# ============================================================
# TESTE 1
# ============================================================

def test_system_prompt_exists():

    assert isinstance(
        SYSTEM_PROMPT,
        str,
    )

    assert SYSTEM_PROMPT.strip()


# ============================================================
# TESTE 2
# ============================================================

def test_user_prompt_template_exists():

    assert isinstance(
        USER_PROMPT_TEMPLATE,
        str,
    )

    assert "{query}" in USER_PROMPT_TEMPLATE

    assert "{context}" in USER_PROMPT_TEMPLATE


# ============================================================
# TESTE 3
# ============================================================

def test_build_prompt():

    query = "O que é a Reforma Tributária?"

    context = (
        "Documento: Modulo_1_parte_1.pdf\n"
        "Página: 10\n"
        "Conteúdo sobre Reforma Tributária."
    )

    prompt = build_prompt(
        query=query,
        context=context,
    )

    assert isinstance(
        prompt,
        str,
    )

    assert query in prompt

    assert context in prompt


# ============================================================
# TESTE 4
# ============================================================

def test_build_prompt_contains_instructions():

    prompt = build_prompt(
        query="O que é a Reforma Tributária?",
        context="Conteúdo oficial.",
    )

    assert "Responda diretamente à pergunta" in prompt

    assert "Baseie a resposta exclusivamente" in prompt

    assert "documento" in prompt.lower()

    assert "página" in prompt.lower()


# ============================================================
# TESTE 5
# ============================================================

def test_build_prompt_strips_query_and_context():

    prompt = build_prompt(
        query="   Reforma Tributária   ",
        context="   Conteúdo oficial.   ",
    )

    assert "Reforma Tributária" in prompt

    assert "Conteúdo oficial." in prompt


# ============================================================
# TESTE 6
# ============================================================

def test_build_prompt_invalid_query_type():

    with pytest.raises(TypeError):

        build_prompt(
            query=123,
            context="Contexto",
        )


# ============================================================
# TESTE 7
# ============================================================

def test_build_prompt_invalid_context_type():

    with pytest.raises(TypeError):

        build_prompt(
            query="Pergunta",
            context=123,
        )


# ============================================================
# TESTE 8
# ============================================================

def test_build_prompt_empty_query():

    with pytest.raises(ValueError):

        build_prompt(
            query="",
            context="Contexto",
        )


# ============================================================
# TESTE 9
# ============================================================

def test_build_prompt_whitespace_query():

    with pytest.raises(ValueError):

        build_prompt(
            query="   ",
            context="Contexto",
        )


# ============================================================
# TESTE 10
# ============================================================

def test_build_prompt_empty_context():

    with pytest.raises(ValueError):

        build_prompt(
            query="Pergunta",
            context="",
        )


# ============================================================
# TESTE 11
# ============================================================

def test_build_prompt_whitespace_context():

    with pytest.raises(ValueError):

        build_prompt(
            query="Pergunta",
            context="   ",
        )


# ============================================================
# TESTE 12
# ============================================================

def test_build_messages():

    messages = build_messages(
        query="O que é a Reforma Tributária?",
        context="Conteúdo oficial.",
    )

    assert isinstance(
        messages,
        list,
    )

    assert len(messages) == 2


# ============================================================
# TESTE 13
# ============================================================

def test_build_messages_roles():

    messages = build_messages(
        query="O que é a Reforma Tributária?",
        context="Conteúdo oficial.",
    )

    assert messages[0]["role"] == "system"

    assert messages[1]["role"] == "user"


# ============================================================
# TESTE 14
# ============================================================

def test_build_messages_contains_system_prompt():

    messages = build_messages(
        query="O que é a Reforma Tributária?",
        context="Conteúdo oficial.",
    )

    assert messages[0]["content"] == SYSTEM_PROMPT


# ============================================================
# TESTE 15
# ============================================================

def test_build_messages_contains_query():

    query = "O que é a Reforma Tributária?"

    messages = build_messages(
        query=query,
        context="Conteúdo oficial.",
    )

    assert query in messages[1]["content"]


# ============================================================
# TESTE 16
# ============================================================

def test_build_messages_contains_context():

    context = (
        "Documento: Modulo_1_parte_1.pdf\n"
        "Página: 10\n"
        "Conteúdo oficial."
    )

    messages = build_messages(
        query="Pergunta",
        context=context,
    )

    assert context in messages[1]["content"]


# ============================================================
# TESTE 17
# ============================================================

def test_build_messages_invalid_query():

    with pytest.raises(TypeError):

        build_messages(
            query=123,
            context="Contexto",
        )


# ============================================================
# TESTE 18
# ============================================================

def test_build_messages_invalid_context():

    with pytest.raises(TypeError):

        build_messages(
            query="Pergunta",
            context=123,
        )