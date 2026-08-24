from __future__ import annotations

import streamlit as st

from app.agent import create_agent


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Reforma Tributária | AI Agent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# TEMA ESCURO
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       FUNDO PRINCIPAL
       ======================================================== */

    .stApp {
        background: #0b1120;
        color: #e5e7eb;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }


    /* ========================================================
       TÍTULOS
       ======================================================== */

    h1, h2, h3 {
        color: #f8fafc !important;
    }


    /* ========================================================
       CABEÇALHO
       ======================================================== */

    .hero {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 20px;
        padding: 2.2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.6rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        line-height: 1.6;
    }

    .hero-status {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        background: #052e16;
        border: 1px solid #166534;
        color: #86efac;
        font-size: 0.8rem;
        font-weight: 600;
    }


    /* ========================================================
       CARDS
       ======================================================== */

    [data-testid="column"] {
        background: #111827;
        border-radius: 14px;
    }


    /* ========================================================
       CHAT
       ======================================================== */

    [data-testid="stChatMessage"] {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
    }


    /* ========================================================
       INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        background: #111827;
    }

    [data-testid="stChatInput"] textarea {
        background: #1f2937 !important;
        color: #f8fafc !important;
        border: 1px solid #374151 !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 12px;
    }


    /* ========================================================
       ALERTAS
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ========================================================
       RODAPÉ
       ======================================================== */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
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
    """
    <div class="hero">

        <div class="hero-title">
            ⚖️ Reforma Tributária | AI Agent
        </div>

        <div class="hero-subtitle">
            Assistente inteligente para consulta,
            interpretação e compreensão da Reforma Tributária
            com base em documentos oficiais.
        </div>

        <div class="hero-status">
            ● RAG conectado
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("📚 Base documental")

    st.write(
        "Respostas fundamentadas em documentos oficiais "
        "e materiais selecionados sobre a Reforma Tributária."
    )


with col2:

    st.subheader("🔎 Busca inteligente")

    st.write(
        "Recuperação dos trechos mais relevantes "
        "utilizando arquitetura RAG."
    )


with col3:

    st.subheader("📖 Respostas com fontes")

    st.write(
        "Consulte os documentos e páginas utilizados "
        "para fundamentar cada resposta."
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Configurações")

    st.subheader("📚 Base de conhecimento")

    st.success("RAG conectado")

    st.write("Fontes documentais:")

    st.write("• Receita Federal")
    st.write("• CFC")
    st.write("• Fenacon")
    st.write("• Documentos oficiais")

    st.divider()

    st.subheader("🔎 Recuperação")

    k = st.slider(
        "Documentos recuperados",
        min_value=1,
        max_value=10,
        value=5,
    )

    st.divider()

    st.subheader("ℹ️ Sobre o agente")

    st.write(
        "Este assistente utiliza uma arquitetura "
        "Retrieval-Augmented Generation (RAG) para "
        "consultar a base documental antes de gerar "
        "uma resposta."
    )

    st.divider()

    st.caption(
        "Reforma Tributária | AI Agent"
    )


# ============================================================
# HISTÓRICO
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# TELA INICIAL
# ============================================================

if not st.session_state.messages:

    st.header("👋 Como posso ajudar?")

    st.write(
        "Faça uma pergunta sobre a "
        "**Reforma Tributária do Consumo**."
    )

    st.write("### Exemplos")

    st.info("O que é o IBS?")

    st.info("O que é a CBS?")

    st.info("Como funciona a transição?")

    st.info("Quais são os impactos para empresas?")

    st.info("O que muda na tributação do consumo?")


# ============================================================
# EXIBE HISTÓRICO
# ============================================================

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
                            "section",
                            "",
                        )

                        organization = source.get(
                            "source_organization",
                            "N/A",
                        )

                        st.markdown(
                            f"**📄 Documento:** {document_name}"
                        )

                        st.markdown(
                            f"**🏢 Instituição:** {organization}"
                        )

                        st.markdown(
                            f"**📖 Página:** {page}"
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
    # PERGUNTA
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )


    # --------------------------------------------------------
    # RESPOSTA
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
                                "section",
                                "",
                            )

                            organization = source.get(
                                "source_organization",
                                "N/A",
                            )

                            st.markdown(
                                f"**📄 Documento:** {document_name}"
                            )

                            st.markdown(
                                f"**🏢 Instituição:** {organization}"
                            )

                            st.markdown(
                                f"**📖 Página:** {page}"
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
                # SALVA HISTÓRICO
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


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "⚖️ Reforma Tributária | AI Agent · Arquitetura RAG · Consulta baseada em documentos oficiais"
)