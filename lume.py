import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Carrega a chave da API do arquivo .env
load_dotenv()

print("Despertando o Lume...")

# 2. Conecta ao Banco Vetorial (Memória)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
banco_vetorial = Chroma(persist_directory="./db", embedding_function=embeddings)
retriever = banco_vetorial.as_retriever(search_kwargs={"k": 6})

# 3. Configura o LLM do Gemini (Voz)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# 4. Define a Personalidade e o Prompt do Lume
template = """Você é o Lume, o assistente virtual inteligente da WeNove, um marketplace de moda circular.
Use APENAS os pedaços de contexto recuperados a seguir para responder à pergunta do usuário.
Se a resposta não estiver no contexto, diga gentilmente que não tem essa informação. Não tente inventar.
Seja claro, direto e profissional.

Contexto recuperado:
{context}

Pergunta do usuário: {question}

Resposta:"""

prompt = ChatPromptTemplate.from_template(template)

# Função auxiliar para organizar os textos encontrados
def formatar_documentos(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Cria a estrutura moderna do LangChain (LCEL) sem usar o módulo antigo 'chains'
rag_chain = (
    {"context": retriever | formatar_documentos, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("\n=======================================================")
print("🟢 Lume Online! (Digite 'sair' para encerrar o chat)")
print("=======================================================\n")

# 5. Loop de conversa no terminal
while True:
    pergunta = input("Você: ")
    
    if pergunta.lower() == 'sair':
        print("Lume: Até logo! Encerrando o sistema...")
        break
        
    if not pergunta.strip():
        continue
        
    print("Lume está pensando...")
    
    try:
        # Envia a pergunta para a IA formular a resposta final
        resposta = rag_chain.invoke(pergunta)
        
        # Faz uma busca rápida apenas para descobrir de quais arquivos a informação saiu
        docs_recuperados = retriever.invoke(pergunta)
        fontes = set([doc.metadata['fonte'] for doc in docs_recuperados])
        
        print(f"\nLume: {resposta}")
        print(f"\n[Fontes consultadas: {', '.join(fontes)}]\n")
        print("-" * 50)
        
    except Exception as e:
        print(f"\n[Erro de conexão com a IA]: Verifique sua chave no arquivo .env ou a conexão com a internet. Detalhes: {e}\n")