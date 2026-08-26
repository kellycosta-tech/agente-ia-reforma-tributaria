from __future__ import annotations

import os
import sys

import streamlit as st

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

APP_DIR = os.path.dirname(os.path.abspath(__file__))

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from app.agent import create_agent
from app.llm import LLMQuotaError
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
# CONTROLE DE TEMA
# ============================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode


button_icon = (
    "☀️"
    if st.session_state.dark_mode
    else "🌙"
)

# ============================================================
# TEMA VISUAL
# ============================================================

if st.session_state.dark_mode:

    bg_global = "#0F172A"
    text_main = "#F8FAFC"
    card_bg = "#1E293B"
    input_bg = "#0F172A"
    border = "rgba(255, 255, 255, 0.10)"
    secondary_text = "#CBD5E1"

else:

    bg_global = "#F5F1EB"
    text_main = "#011E38"
    card_bg = "#FFFFFF"
    input_bg = "#FFFFFF"
    border = "rgba(1, 30, 56, 0.15)"
    secondary_text = "#475569"


st.markdown(
    f"""
    <style>

    /* ========================================================
       PALETA
       ======================================================== */

    :root {{
        --gb-blue-deep: #011E38;
        --gb-blue-action: #264FEC;
        --gb-salmon: #FFBC82;
        --gb-off-white: #F5F1EB;
        --gb-success: #27AE60;
        --gb-danger: #C70E0E;

        --bg-global: {bg_global};
        --text-main: {text_main};
        --card-bg: {card_bg};
        --input-bg: {input_bg};
        --border: {border};
        --secondary-text: {secondary_text};
    }}


    /* ========================================================
       FUNDO PRINCIPAL
       ======================================================== */

    .stApp {{
        background-color: var(--bg-global) !important;
        color: var(--text-main) !important;
    }}

    .main .block-container {{
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }}


    /* ========================================================
       TEXTO GERAL
       ======================================================== */

    .stApp p,
    .stApp span,
    .stApp label,
    .stApp li,
    .stApp td,
    .stApp th,
    .stApp strong,
    .stApp em {{
        color: var(--text-main) !important;
    }}

    h1,
    h2,
    h3 {{
        color: var(--text-main) !important;
    }}

    /* ========================================================
       CONTEÚDO DAS RESPOSTAS DO CHAT
       ======================================================== */

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] em,
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] h4,
    [data-testid="stChatMessage"] h5,
    [data-testid="stChatMessage"] h6 {{
        color: var(--text-main) !important;
    }}

    [data-testid="stChatMessage"] a {{
        color: var(--gb-blue-action) !important;
    }}

    [data-testid="stChatMessage"] blockquote {{
        color: var(--secondary-text) !important;
        border-left: 4px solid var(--gb-blue-action) !important;
    }}

    [data-testid="stChatMessage"] code {{
        color: var(--text-main) !important;
        background-color: var(--input-bg) !important;
    }}

    [data-testid="stChatMessage"] pre {{
        background-color: var(--input-bg) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border) !important;
    }}

    /* ========================================================
       TABELAS NAS RESPOSTAS
       ======================================================== */

    [data-testid="stChatMessage"] table {{
        color: var(--text-main) !important;
        background-color: var(--card-bg) !important;
    }}

    [data-testid="stChatMessage"] thead th {{
        color: var(--text-main) !important;
        background-color: var(--input-bg) !important;
        border-color: var(--border) !important;
    }}

    [data-testid="stChatMessage"] tbody td {{
        color: var(--text-main) !important;
        border-color: var(--border) !important;
    }}
    
    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {{
        background-color: var(--gb-blue-deep) !important;
        border-right: 1px solid rgba(255,255,255,0.10);
    }}

    section[data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}


    /* ========================================================
       BOTÃO DE TEMA
       ======================================================== */

    div[data-testid="stButton"] button {{
        background-color: var(--gb-blue-action) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 50% !important;

        width: 48px !important;
        height: 48px !important;

        padding: 0 !important;

        font-size: 1.2rem !important;

        box-shadow:
            0 8px 24px rgba(0,0,0,0.20);

        transition:
            transform 0.2s ease,
            background-color 0.2s ease;
    }}

    div[data-testid="stButton"] button:hover {{
        background-color: var(--gb-blue-deep) !important;
        color: var(--gb-salmon) !important;
        transform: scale(1.05);
    }}


    /* ========================================================
       CABEÇALHO
       ======================================================== */

    .hero {{
        background-color: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 20px;

        padding: 2.2rem;
        margin-bottom: 1.5rem;

        text-align: center;

        box-shadow:
            0 10px 30px rgba(1,30,56,0.08);
    }}

    .hero-title {{
        font-size: 2.2rem;
        font-weight: 800;

        color: var(--gb-blue-action) !important;

        margin-bottom: 0.6rem;
    }}

    .hero-subtitle {{
        font-size: 1rem;
        color: var(--secondary-text) !important;

        line-height: 1.6;
    }}

    .hero-status {{
        display: inline-block;

        margin-top: 1rem;

        padding: 0.35rem 0.8rem;

        border-radius: 20px;

        background: rgba(39,174,96,0.12);

        border:
            1px solid rgba(39,174,96,0.30);

        color: var(--gb-success) !important;

        font-size: 0.8rem;
        font-weight: 600;
    }}


    /* ========================================================
       CARDS
       ======================================================== */

    [data-testid="column"] {{
        background-color: var(--card-bg);

        border:
            1px solid var(--border);

        border-radius: 14px;

        padding: 1rem;
    }}

    .info-card {{
        padding: 0.5rem;
    }}

    .info-icon {{
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }}

    .info-title {{
        color: var(--text-main) !important;

        font-size: 1rem;
        font-weight: 700;

        margin-bottom: 0.4rem;
    }}

    .info-text {{
        color: var(--secondary-text) !important;

        font-size: 0.9rem;

        line-height: 1.5;
    }}


    /* ========================================================
       TELA INICIAL
       ======================================================== */

    .welcome {{
        background-color: var(--card-bg);

        border:
            1px solid var(--border);

        border-radius: 18px;

        padding: 2rem;

        margin-top: 1.5rem;
        margin-bottom: 2rem;

        box-shadow:
            0 10px 30px rgba(1,30,56,0.05);
    }}

    .welcome-title {{
        color: var(--text-main) !important;

        font-size: 1.6rem;
        font-weight: 750;

        margin-bottom: 0.6rem;
    }}

    .welcome-text {{
        color: var(--secondary-text) !important;

        font-size: 1rem;

        line-height: 1.6;

        margin-bottom: 1.5rem;
    }}

    .examples-title {{
        color: var(--gb-blue-action) !important;

        font-size: 0.9rem;

        font-weight: 700;

        margin-bottom: 0.8rem;
    }}

    .examples {{
        display: flex;

        flex-wrap: wrap;

        gap: 0.7rem;
    }}

    .example {{
        background-color:
            rgba(38,79,236,0.08);

        border:
            1px solid var(--border);

        color: var(--text-main) !important;

        padding: 0.65rem 0.9rem;

        border-radius: 10px;

        font-size: 0.85rem;
    }}


    /* ========================================================
       CHAT
       ======================================================== */

    [data-testid="stChatMessage"] {{
        background-color: var(--card-bg);

        border:
            1px solid var(--border);

        border-radius: 14px;

        padding: 0.8rem;

        margin-bottom: 0.8rem;
    }}


    /* ========================================================
       CAMPO DE PERGUNTA
       ======================================================== */

    [data-testid="stChatInput"] {{
        background-color: var(--card-bg);
    }}

    [data-testid="stChatInput"] textarea {{
        background-color: var(--input-bg) !important;

        color: var(--text-main) !important;

        border:
            1px solid var(--border) !important;
    }}

    [data-testid="stChatInput"] textarea::placeholder {{
        color: #64748B !important;
    }}


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {{
        background-color: var(--card-bg);

        border:
            1px solid var(--border);

        border-radius: 12px;
    }}


    /* ========================================================
       ALERTAS
       ======================================================== */

    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}


    /* ========================================================
       RODAPÉ
       ======================================================== */

    .footer {{
        text-align: center;

        color: var(--secondary-text) !important;

        font-size: 0.8rem;

        margin-top: 3rem;

        padding: 1rem;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# BOTÃO DE TEMA
# ============================================================

col_theme, _ = st.columns([1, 12])

with col_theme:

    st.button(
        button_icon,
        key="theme_toggle",
        help="Alternar entre tema claro e escuro",
        on_click=toggle_theme,
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

st.html(
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
    """
)


# ============================================================
# CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">📚</div>
            <div class="info-title">Base documental</div>
            <div class="info-text">
                Respostas fundamentadas em documentos oficiais
                e materiais selecionados sobre a Reforma Tributária.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">🔎</div>
            <div class="info-title">Busca inteligente</div>
            <div class="info-text">
                Recuperação dos trechos mais relevantes
                utilizando arquitetura RAG.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">📖</div>
            <div class="info-title">Respostas com fontes</div>
            <div class="info-text">
                Consulte os documentos e páginas utilizados
                para fundamentar cada resposta.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
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

    st.html(
        """
        <div class="welcome">

            <div class="welcome-title">
                👋 Como posso ajudar?
            </div>

            <div class="welcome-text">
                Faça uma pergunta sobre a
                <strong>Reforma Tributária do Consumo</strong>.
            </div>

            <div class="examples-title">
                Exemplos de perguntas
            </div>

            <div class="examples">

                <div class="example">
                    O que é o IBS?
                </div>

                <div class="example">
                    O que é a CBS?
                </div>

                <div class="example">
                    Como funciona a transição?
                </div>

                <div class="example">
                    Quais são os impactos para empresas?
                </div>

                <div class="example">
                    O que muda na tributação do consumo?
                </div>

            </div>

        </div>
        """
    )

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

            # --------------------------------------------
            # QUOTA / RATE LIMIT GEMINI
            # --------------------------------------------

            except LLMQuotaError:

                st.warning(
                    "⚠️ **Limite temporário da IA**\n\n"
                    "O serviço de IA atingiu temporariamente "
                    "o limite de requisições da API Gemini.\n\n"
                    "Aguarde alguns instantes e tente novamente."
                )

            # --------------------------------------------
            # OUTROS ERROS
            # --------------------------------------------

            except Exception as exc:

                st.error(
                    "❌ Ocorreu um erro ao processar a pergunta."
                )

                with st.expander(
                    "🔎 Detalhes técnicos"
                ):

                    st.code(
                        str(exc)
                    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "⚖️ Reforma Tributária | AI Agent · Arquitetura RAG · Consulta baseada em documentos oficiais"
)
