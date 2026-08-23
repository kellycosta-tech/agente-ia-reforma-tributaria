"""
Testes da camada de LLM.

Valida:

    BaseLLM
       ↓
    FakeLLM
       ↓
    geração de respostas
"""


import pytest

from app.llm import (
    BaseLLM,
    FakeLLM,
    create_llm,
)


# ============================================================
# TESTE 1
# ============================================================

def test_fake_llm_is_llm():

    llm = FakeLLM()

    assert isinstance(
        llm,
        BaseLLM,
    )


# ============================================================
# TESTE 2
# ============================================================

def test_fake_llm_generate():

    llm = FakeLLM(
        response="Resposta de teste."
    )

    response = llm.generate(
        "O que é a Reforma Tributária?"
    )

    assert isinstance(
        response,
        str,
    )

    assert response == (
        "Resposta de teste."
    )


# ============================================================
# TESTE 3
# ============================================================

def test_fake_llm_preserves_custom_response():

    response = (
        "A Reforma Tributária altera "
        "a tributação sobre o consumo."
    )

    llm = FakeLLM(
        response=response,
    )

    result = llm.generate(
        "Explique a Reforma Tributária."
    )

    assert result == response


# ============================================================
# TESTE 4
# ============================================================

def test_fake_llm_invalid_response_type():

    with pytest.raises(TypeError):

        FakeLLM(
            response=123,
        )


# ============================================================
# TESTE 5
# ============================================================

def test_fake_llm_empty_response():

    with pytest.raises(ValueError):

        FakeLLM(
            response="",
        )


# ============================================================
# TESTE 6
# ============================================================

def test_fake_llm_whitespace_response():

    with pytest.raises(ValueError):

        FakeLLM(
            response="   ",
        )


# ============================================================
# TESTE 7
# ============================================================

def test_fake_llm_invalid_prompt_type():

    llm = FakeLLM()

    with pytest.raises(TypeError):

        llm.generate(
            123,
        )


# ============================================================
# TESTE 8
# ============================================================

def test_fake_llm_empty_prompt():

    llm = FakeLLM()

    with pytest.raises(ValueError):

        llm.generate(
            "",
        )


# ============================================================
# TESTE 9
# ============================================================

def test_fake_llm_whitespace_prompt():

    llm = FakeLLM()

    with pytest.raises(ValueError):

        llm.generate(
            "   ",
        )


# ============================================================
# TESTE 10
# ============================================================

def test_create_llm():

    llm = create_llm()

    assert llm is not None

    assert isinstance(
        llm,
        BaseLLM,
    )


# ============================================================
# TESTE 11
# ============================================================

def test_create_llm_generates_response():

    llm = create_llm()

    response = llm.generate(
        "Explique a Reforma Tributária."
    )

    assert isinstance(
        response,
        str,
    )

    assert response.strip()


# ============================================================
# TESTE 12
# ============================================================

def test_llm_can_receive_rag_prompt():

    llm = FakeLLM(
        response=(
            "A resposta foi baseada "
            "no contexto recuperado."
        ),
    )

    prompt = """
    Pergunta:
    O que é a Reforma Tributária?

    Contexto:
    Documento oficial sobre Reforma Tributária.
    Página 10.
    """

    response = llm.generate(
        prompt,
    )

    assert response == (
        "A resposta foi baseada "
        "no contexto recuperado."
    )