from __future__ import annotations

import streamlit as st

from app.agent import create_agent


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Reforma Tributária AI Agent",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>
        .main {
            padding-top: 2rem;
        }

        .title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }

        .subtitle {
            color: #666;
            font-size: 1.05rem;
            margin-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AGENTE
# ============================================================

@st.cache_resource
def load_agent():
    return create_agent()


try:
    agent = load_agent()
except Exception as exc:
    st.error("❌ Não foi possível inicializar o agente.")
    st.exception(exc)
    st.stop()


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="title">🤖 Reforma Tributária AI Agent</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Agente de IA para consulta e apoio à compreensão "
    "da Reforma Tributária."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Configurações")

    st.markdown("### 📚 Base de conhecimento")

    st.success("RAG conectado")

    st.markdown(
        """
        **Fontes documentais**

        - Receita Federal
        - CFC
        - Fenacon
        - Documentos oficiais
        """
    )

    st.divider()

    st.markdown("### 🔎 Recuperação")

    k = st.slider(
        "Quantidade de documentos recuperados",
        min_value=1,
        max_value=10,
        value=5,
    )

    st.divider()

    st.caption(
        "As respostas são geradas a partir dos documentos "
        "recuperados pela camada RAG."
    )


# ============================================================
# HISTÓRICO
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            sources = message.get(
                "sources",
                [],
            )

            if sources:

                with st.expander(
                    "📚 Fontes utilizadas"
                ):

                    for source in sources:

                        document_name = source.get(
                            "document_name",
                            "Documento não informado",
                        )

                        page = source.get(
                            "page",
                            "N/A",
                        )

                        section = source.get(
                            "section"
                        )

                        organization = source.get(
                            "source_organization",
                            "N/A",
                        )

                        st.markdown(
                            f"""
                            **📄 Documento:** {document_name}

                            **🏢 Instituição:** {organization}

                            **📖 Página:** {page}
                            """
                        )

                        if section:
                            st.markdown(
                                f"**📌 Seção:** {section}"
                            )

                        st.divider()


# ============================================================
# PERGUNTA
# ============================================================

question = st.chat_input(
    "Digite sua pergunta sobre a Reforma Tributária..."
)


# ============================================================
# PROCESSAMENTO
# ============================================================

if question:

    # --------------------------------------------------------
    # Exibe pergunta
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)

    # --------------------------------------------------------
    # Salva pergunta
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # --------------------------------------------------------
    # Executa Agent
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Consultando a base documental..."
        ):

            try:

                result = agent.ask(
                    query=question,
                    k=k,
                )

                answer = result.get(
                    "answer",
                    "",
                )

                sources = result.get(
                    "sources",
                    [],
                )

                # --------------------------------------------
                # RESPOSTA
                # --------------------------------------------

                st.markdown(answer)

                # --------------------------------------------
                # FONTES
                # --------------------------------------------

                if sources:

                    with st.expander(
                        "📚 Fontes utilizadas"
                    ):

                        for source in sources:

                            document_name = source.get(
                                "document_name",
                                "Documento não informado",
                            )

                            page = source.get(
                                "page",
                                "N/A",
                            )

                            section = source.get(
                                "section"
                            )

                            organization = source.get(
                                "source_organization",
                                "N/A",
                            )

                            st.markdown(
                                f"""
                                **📄 Documento:** {document_name}

                                **🏢 Instituição:** {organization}

                                **📖 Página:** {page}
                                """
                            )

                            if section:

                                st.markdown(
                                    f"**📌 Seção:** {section}"
                                )

                            st.divider()

                else:

                    st.info(
                        "Nenhuma fonte foi retornada."
                    )

                # --------------------------------------------
                # SALVA RESPOSTA
                # --------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except Exception as exc:

                st.error(
                    "❌ Ocorreu um erro ao processar a pergunta."
                )

                st.exception(exc)