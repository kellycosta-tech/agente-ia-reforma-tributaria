"""
Camada de abstração para modelos de linguagem (LLM).

Responsabilidades:

    1. Definir uma interface comum para LLMs.
    2. Receber pergunta + contexto.
    3. Gerar uma resposta.
    4. Permitir futuras integrações com diferentes provedores.

Nesta etapa, nenhuma API externa é chamada diretamente.

Fluxo:

    Pergunta
       ↓
    RAG / Contexto
       ↓
    Prompt
       ↓
    LLM
       ↓
    Resposta
"""


from __future__ import annotations

from abc import ABC, abstractmethod


# ============================================================
# LLM BASE
# ============================================================

class BaseLLM(ABC):
    """
    Interface base para modelos de linguagem.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Gera uma resposta a partir de um prompt.

        Parameters
        ----------
        prompt:
            Prompt enviado ao modelo.

        Returns
        -------
        str
            Resposta gerada pelo modelo.
        """

        raise NotImplementedError


# ============================================================
# FAKE / MOCK LLM
# ============================================================

class FakeLLM(BaseLLM):
    """
    LLM simulada para testes.

    Não realiza chamadas externas.
    """

    def __init__(
        self,
        response: str = (
            "Resposta simulada baseada no contexto fornecido."
        ),
    ) -> None:

        if not isinstance(response, str):
            raise TypeError(
                "response deve ser uma string."
            )

        response = response.strip()

        if not response:
            raise ValueError(
                "response não pode estar vazia."
            )

        self.response = response

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Retorna uma resposta simulada.
        """

        if not isinstance(prompt, str):
            raise TypeError(
                "prompt deve ser uma string."
            )

        prompt = prompt.strip()

        if not prompt:
            raise ValueError(
                "prompt não pode estar vazio."
            )

        return self.response


# ============================================================
# LLM FACTORY
# ============================================================

def create_llm() -> BaseLLM:
    """
    Cria uma instância padrão de LLM.

    Nesta etapa do projeto, utiliza FakeLLM para permitir
    testes sem dependência de serviços externos.

    A implementação poderá ser substituída posteriormente
    por um provedor real de LLM.
    """

    return FakeLLM()