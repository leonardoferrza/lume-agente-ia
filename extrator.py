import os
import json
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader

def extrair_texto(caminho_arquivo):
    """Lê o arquivo dependendo da sua extensão e retorna o texto puro."""
    extensao = os.path.splitext(caminho_arquivo)[1].lower()
    texto_extraido = ""
    
    try:
        if extensao == '.json':
            # Lê o FAQ e formata como Pergunta e Resposta
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                for item in dados:
                    texto_extraido += f"Pergunta: {item.get('pergunta', '')}\nResposta: {item.get('resposta', '')}\n\n"
                    
        elif extensao == '.md':
            # Markdown é lido como texto normal
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                texto_extraido = f.read()
                
        elif extensao == '.csv':
            # Transforma as linhas da planilha em frases de linguagem natural para a IA entender melhor
            df = pd.read_csv(caminho_arquivo)
            linhas_texto = []
            
            for index, row in df.iterrows():
                frase = (f"Regra da WeNove para a categoria '{row['Categoria']}': "
                         f"A condição aceita é '{row['Condicao_Aceita']}'. "
                         f"A taxa de comissão retida pela WeNove é de {row['Taxa_Comissao_WeNove']}. "
                         f"A taxa de logística fixa cobrada é de {row['Taxa_Logistica_Fixa']}. "
                         f"O tempo máximo que a peça fica na vitrine é de {row['Tempo_Maximo_Vitrine_Dias']} dias.")
                linhas_texto.append(frase)
                
            texto_extraido = "\n\n".join(linhas_texto)
            
        elif extensao == '.docx':
            # Lê os parágrafos do arquivo Word (Jurídico)
            doc = Document(caminho_arquivo)
            texto_extraido = "\n".join([paragrafo.text for paragrafo in doc.paragraphs])
            
        elif extensao == '.pdf':
            # Extrai texto de cada página do PDF (RH)
            leitor = PdfReader(caminho_arquivo)
            for pagina in leitor.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_extraido += texto + "\n"
                    
        else:
            texto_extraido = f"Formato não suportado: {extensao}"
            
    except Exception as e:
        print(f"Erro ao ler {caminho_arquivo}: {e}")
        
    return texto_extraido.strip()

# Bloco de teste: Executa a leitura quando rodamos o arquivo
if __name__ == "__main__":
    pasta_dados = 'dados'
    
    print("Iniciando a extração de documentos da WeNove...\n")
    
    # Varre todas as pastas e subpastas dentro de 'dados'
    for raiz, _, arquivos in os.walk(pasta_dados):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            texto = extrair_texto(caminho_completo)
            
            print(f"--- Arquivo lido: {arquivo} ---")
            # Imprime os primeiros 150 caracteres para provar que funcionou sem poluir o terminal
            print(texto[:150] + " [...]\n")