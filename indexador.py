import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from extrator import extrair_texto 

def criar_banco_vetorial():
    pasta_dados = 'dados'
    documentos = []
    metadados = []

    print("1. Lendo os arquivos e extraindo textos...")
    for raiz, _, arquivos in os.walk(pasta_dados):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            texto = extrair_texto(caminho_completo)
            
            if texto:
                documentos.append(texto)
                # Guardamos o nome do arquivo para a IA citar a fonte depois!
                metadados.append({"fonte": arquivo})

    print("2. Quebrando os textos em pedaços menores (Chunking)...")
    # Divide o texto em blocos de 500 caracteres, com 50 de sobreposição (overlap)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    chunks = []
    chunks_metadados = []
    
    for i, doc in enumerate(documentos):
        pedacos = text_splitter.split_text(doc)
        chunks.extend(pedacos)
        # Copia o nome do arquivo para cada pedacinho gerado
        chunks_metadados.extend([metadados[i]] * len(pedacos))

    print(f"Total de pedaços (chunks) gerados: {len(chunks)}")

    print("3. Gerando os vetores (Embeddings) e salvando no ChromaDB...")
    # Usa um modelo gratuito, leve e rápido para transformar texto em números
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Cria e salva o banco vetorial na pasta 'db'
    banco_vetorial = Chroma.from_texts(
        texts=chunks, 
        embedding=embeddings, 
        metadatas=chunks_metadados,
        persist_directory="./db"
    )
    
    print("\n✅ Sucesso! O 'cérebro' do Lume foi criado na pasta 'db'.")

if __name__ == "__main__":
    criar_banco_vetorial()