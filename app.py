import streamlit as st
import os
import io
import pandas as pd
import speech_recognition as sr
from operator import itemgetter
from dotenv import load_dotenv
from gtts import gTTS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ==========================================
# 0. Configuração Geral e UI 
# ==========================================
st.set_page_config(page_title="Lume | WeNove", page_icon="🌱", layout="centered")

st.markdown("""
    <style>
        .stApp { background-color: #FAFAFA; }
        [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E0E0E0; }
        .lume-header {
            display:flex; align-items:center; gap:.4rem;
            font-size: 1.2rem; color:#1A3626; font-weight:600;
            margin-bottom: 1rem;
        }
        /* HACK DE UI: Arrastar as ferramentas para cima do Input */
        .ferramentas-flutuantes {
            position: fixed;
            bottom: 30px; 
            right: 4rem; 
            z-index: 9999; 
            display: flex;
            gap: 10px;
            background-color: transparent;
        }
        .ferramentas-flutuantes [data-testid="stPopover"] button {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            font-size: 1.2rem;
            padding: 0;
            color: #5F6368;
        }
        .ferramentas-flutuantes [data-testid="stPopover"] button:hover {
            color: #1A3626;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. Motor de IA (RAG)
# ==========================================
@st.cache_resource
def iniciar_lume():
    load_dotenv()
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    banco_vetorial = Chroma(persist_directory="./db", embedding_function=embeddings)
    retriever = banco_vetorial.as_retriever(search_kwargs={"k": 6})
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

    template = """Você é o Lume, o assistente virtual da WeNove (marketplace de moda circular).
    
    Regras:
    1. Se o usuário disser "oi", "olá", apresente-se amigavelmente.
    2. Use o TEXTO DE ARQUIVO ANEXO (se houver) para complementar a resposta.
    3. Para dúvidas técnicas, use APENAS o contexto recuperado. Não invente.
    
    Texto de Arquivo Anexo: {arquivo_contexto}
    Contexto recuperado: {context}
    Pergunta do usuário: {question}
    Resposta:"""

    prompt = ChatPromptTemplate.from_template(template)

    def formatar_documentos(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": itemgetter("question") | retriever | formatar_documentos, 
            "question": itemgetter("question"), 
            "arquivo_contexto": itemgetter("arquivo_contexto")
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain, retriever

rag_chain, retriever = iniciar_lume()

def gerar_audio(texto):
    texto_limpo = texto.replace('*', '').replace('#', '')
    tts = gTTS(text=texto_limpo, lang='pt-br', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# ==========================================
# 2. Estado da Conversa
# ==========================================
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "texto_arquivo" not in st.session_state:
    st.session_state.texto_arquivo = ""

def limpar_conversa():
    st.session_state.mensagens = []
    st.session_state.texto_arquivo = ""

# ==========================================
# 3. Aba Lateral 
# ==========================================
with st.sidebar:
    st.markdown("### 🌱 Lume - WeNove")
    st.button("✏️ Nova conversa", on_click=limpar_conversa, use_container_width=True)

# ==========================================
# 4. Área Principal de Chat
# ==========================================
st.markdown('<div class="lume-header">Lume <span style="color:#9aa0a6; font-weight:400;">· Assistente WeNove</span></div>', unsafe_allow_html=True)

if len(st.session_state.mensagens) == 0:
    st.markdown("### Como posso ajudar você hoje?")
else:
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("audio"):
                st.audio(msg["audio"], format="audio/mp3")

st.write("") 

# ==========================================
# 5. Caixa de Entrada + Ferramentas Flutuantes 
# ==========================================
pergunta = st.chat_input("Pergunte qualquer coisa...")

st.markdown('<div class="ferramentas-flutuantes">', unsafe_allow_html=True)
col_voz, col_anexo = st.columns([1, 1])

# Lógica de Captura de Áudio (Speech-to-Text)
pergunta_por_voz = None
with col_voz:
    with st.popover("🎤"):
        audio_gravado = st.audio_input("Fale sua dúvida", label_visibility="collapsed")
        if audio_gravado:
            r = sr.Recognizer()
            with sr.AudioFile(audio_gravado) as source:
                audio_data = r.record(source)
                try:
                    pergunta_por_voz = r.recognize_google(audio_data, language="pt-BR")
                    st.success(f"Entendido: '{pergunta_por_voz}'")
                except sr.UnknownValueError:
                    st.error("Não entendi o áudio. Tente novamente.")

# Lógica de Upload
with col_anexo:
    with st.popover("📎"):
        arquivo_up = st.file_uploader("TXT ou CSV", type=['txt', 'csv'], label_visibility="collapsed")
        if arquivo_up:
            if arquivo_up.name.endswith('.txt'):
                st.session_state.texto_arquivo = arquivo_up.getvalue().decode('utf-8')
                st.success("Lido!")
            elif arquivo_up.name.endswith('.csv'):
                df = pd.read_csv(arquivo_up)
                st.session_state.texto_arquivo = df.to_string()
                st.success("Lido!")
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. Processamento da Pergunta (Texto ou Voz)
# ==========================================
pergunta_final = pergunta_por_voz if pergunta_por_voz else pergunta

if pergunta_final:
    st.session_state.mensagens.append({"role": "user", "content": pergunta_final})
    with st.chat_message("user"):
        st.markdown(pergunta_final)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Pensando...")

        try:
            resposta_final = rag_chain.invoke({
                "question": pergunta_final,
                "arquivo_contexto": st.session_state.texto_arquivo
            })

            saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]
            if pergunta_final.lower().strip() not in saudacoes:
                docs = retriever.invoke(pergunta_final)
                fontes = set([doc.metadata.get('fonte', 'Desconhecido') for doc in docs])
                texto_fontes = f"\n\n*(Fontes consultadas: {', '.join(fontes)})*"
                resposta_com_fontes = resposta_final + texto_fontes
            else:
                resposta_com_fontes = resposta_final

            placeholder.markdown(resposta_com_fontes)
            
            # Geração do Áudio de Resposta
            audio_gerado = gerar_audio(resposta_final)
            st.audio(audio_gerado, format="audio/mp3", autoplay=True)
            
            st.session_state.mensagens.append({
                "role": "assistant",
                "content": resposta_com_fontes,
                "audio": audio_gerado
            })

        except Exception as e:
            placeholder.markdown(f"**Erro:** {e}")