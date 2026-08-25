"""
Camada de abstração para modelos de linguagem (LLM).

Responsabilidades:

    1. Definir uma interface comum para LLMs.
    2. Receber pergunta + contexto.
    3. Gerar uma resposta.
    4. Permitir diferentes implementações de LLM.
    5. Manter FakeLLM para testes automatizados.
    6. Disponibilizar GeminiLLM para execução real.

Implementações:

    BaseLLM
       │
       ├── FakeLLM
       │      └── Testes
       │
       └── GeminiLLM
              └── Produção / desenvolvimento real

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

import os

from abc import ABC, abstractmethod

from dotenv import load_dotenv
from google import genai


load_dotenv()

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
# GEMINI LLM
# ============================================================

class GeminiLLM(BaseLLM):
    """
    Implementação da interface BaseLLM utilizando a API Gemini.

    A autenticação é realizada por meio da variável de ambiente:

        GEMINI_API_KEY

    O modelo pode ser configurado por:

        GEMINI_MODEL

    Caso não seja informado, utiliza o modelo Flash definido
    como padrão para esta implementação.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:

        # ----------------------------------------------------
        # API KEY
        # ----------------------------------------------------

        api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY não foi configurada."
            )

        if not isinstance(api_key, str):
            raise TypeError(
                "api_key deve ser uma string."
            )

        api_key = api_key.strip()

        if not api_key:
            raise ValueError(
                "api_key não pode estar vazia."
            )

        # ----------------------------------------------------
        # MODELO
        # ----------------------------------------------------

        model = (
            model
            or os.getenv(
                "GEMINI_MODEL",
                "gemini-3.6-flash",
            )
        )

        if not isinstance(model, str):
            raise TypeError(
                "model deve ser uma string."
            )

        model = model.strip()

        if not model:
            raise ValueError(
                "model não pode estar vazio."
            )

        self.model = model

        # ----------------------------------------------------
        # CLIENTE GEMINI
        # ----------------------------------------------------

        self.client = genai.Client(
            api_key=api_key,
        )

    # ========================================================
    # GENERATE
    # ========================================================

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Envia o prompt para o modelo Gemini e retorna a resposta.
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

        # ----------------------------------------------------
        # CHAMADA À API
        # ----------------------------------------------------
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

        except Exception as exc:
            error_text = str(exc)

            # ------------------------------------------------
            # RATE LIMIT / QUOTA GEMINI
            # ------------------------------------------------

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "quota" in error_text.lower()
            ):
                raise RuntimeError(
                    "O serviço de IA atingiu temporariamente "
                    "o limite de requisições da API Gemini. "
                    "Aguarde alguns segundos e tente novamente."
                ) from exc

            # ------------------------------------------------
            # OUTROS ERROS DA API
            # ------------------------------------------------

            raise RuntimeError(
                "Não foi possível obter uma resposta do modelo Gemini."
            ) from exc
        # ----------------------------------------------------
        # VALIDAÇÃO DA RESPOSTA
        # ----------------------------------------------------

        if response is None:
            raise RuntimeError(
                "O Gemini não retornou uma resposta."
            )

        text = getattr(
            response,
            "text",
            None,
        )

        if not isinstance(text, str):
            raise RuntimeError(
                "A resposta do Gemini não contém texto."
            )

        text = text.strip()

        if not text:
            raise RuntimeError(
                "O Gemini retornou uma resposta vazia."
            )

        return text


# ============================================================
# LLM FACTORY
# ============================================================

def create_llm(
    provider: str | None = None,
) -> BaseLLM:
    """
    Cria uma implementação de LLM.

    Providers disponíveis:

        fake
            Utilizado nos testes.

        gemini
            Utilizado para execução real.

    O provider pode ser informado diretamente ou configurado
    pela variável de ambiente:

        LLM_PROVIDER

    Por padrão, utiliza FakeLLM para manter os testes
    independentes de serviços externos.
    """

    provider = (
        provider
        or os.getenv(
            "LLM_PROVIDER",
            "fake",
        )
    )

    if not isinstance(provider, str):
        raise TypeError(
            "provider deve ser uma string."
        )

    provider = provider.strip().lower()

    if provider == "fake":
        return FakeLLM()

    if provider == "gemini":
        return GeminiLLM()

    raise ValueError(
        f"Provider de LLM não suportado: {provider}"
    )