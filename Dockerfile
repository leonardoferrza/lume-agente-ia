# Usa uma imagem oficial do Python leve
FROM python:3.11-slim

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de dependências primeiro
COPY requirements.txt .

# Instala as bibliotecas necessárias (incluindo as de IA e áudio)
RUN pip install --no-cache-dir -r requirements.txt

# Instala dependências do sistema operacional necessárias para o áudio funcionar no Linux da nuvem
RUN apt-get update && apt-get install -y portaudio19-dev build-essential

# Copia todo o resto do seu código (app.py, pasta db, arquivos da WeNove)
COPY . .

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para iniciar o servidor do Lume
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]