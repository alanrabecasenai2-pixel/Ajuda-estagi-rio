import os
import streamlit as st
from openai import AzureOpenAI
import PyPDF2

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Mentor Virtual de Estágio | RAG ChatBot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. CSS Customizado - Visual Moderno, Jovem e Profissional
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #F8FAFC;
    }

    .main .block-container {
        border: 2px solid transparent;
        background-image: linear-gradient(#FFFFFF, #FFFFFF), linear-gradient(135deg, #6366F1, #A855F7, #EC4899);
        background-origin: border-box;
        background-clip: padding-box, border-box;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.1), 0 8px 10px -6px rgba(99, 102, 241, 0.05);
        margin-top: 1rem;
        margin-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E1B4B 0%, #312E81 100%);
        color: #FFFFFF;
    }

    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .main-title {
        background: linear-gradient(90deg, #4F46E5, #7C3AED, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.3rem;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        color: #64748B;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    .badge {
        display: inline-block;
        background: #EEF2FF;
        color: #4F46E5 !important;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }

    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Configuração da API (Microsoft Foundry / Azure OpenAI)
API_KEY = "6t2pTNsmNafDyo53MDAFIrvvQRBZXP7dLcr5j3TLxMS34LQVq3ZUJQQJ99CHACHYHv6XJ3w3AAAAACOGT7os"
DEPLOYMENT_NAME = "gpt-4.1-mini"
ENDPOINT = "https://marcelomaffeis-05082026-resource.services.ai.azure.com/"

try:
    client = AzureOpenAI(
        api_key=API_KEY,
        api_version="2024-08-01-preview",
        azure_endpoint=ENDPOINT
    )
except Exception as e:
    st.error(f"Erro ao inicializar o cliente Azure OpenAI: {e}")

# Inicialização do st.session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

# 3. Barra Lateral (Upload de Arquivos & Guia do Estagiário)
with st.sidebar:
    st.markdown("## 📚 Hub do Estagiário")
    st.markdown("Alimente seu assistente com manuais, procedimentos, tarefas ou apostilas.")
    
    uploaded_file = st.file_uploader("Carregar Arquivo (PDF ou TXT)", type=["pdf", "txt"])
    
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        extracted_text = ""
        
        if file_extension == "txt":
            try:
                extracted_text = uploaded_file.getvalue().decode("utf-8")
            except Exception:
                extracted_text = uploaded_file.getvalue().decode("latin-1")
                
        elif file_extension == "pdf":
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            except Exception as e:
                st.error(f"Erro ao ler o PDF: {e}")
                
        if extracted_text:
            st.session_state.document_text = extracted_text
            st.success(f"⚡ Arquivo '{uploaded_file.name}' pronto para uso!")
        else:
            st.warning("O arquivo enviado parece estar sem texto extraível.")
            
    if st.session_state.document_text:
        if st.button("🗑️ Remover Documento", use_container_width=True):
            st.session_state.document_text = ""
            st.rerun()

    st.markdown("""
        <div class="sidebar-card">
            <h4>💡 Como aproveitar?</h4>
            <ul>
                <li>Envie manuais da empresa ou diretrizes de projetos.</li>
                <li>Tire dúvidas rápidas sem precisar procurar em dezenas de páginas.</li>
                <li>Peça resumos e passos práticos de execução.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# 4. Área Principal (Header & Chat)
st.markdown('<span class="badge">🚀 Programa de Estágio - Assistente IA</span>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Mentor Virtual de Estágio</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Tire suas dúvidas sobre documentos, rotinas e tarefas com o poder da IA do Microsoft Foundry.</p>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.info("👋 **Olá! Sou o seu copiloto de aprendizado.** Mande uma mensagem abaixo ou envie um arquivo de apoio (PDF/TXT) na barra lateral para começarmos!")

for message in st.session_state.messages:
    avatar_icon = "🎓" if message
