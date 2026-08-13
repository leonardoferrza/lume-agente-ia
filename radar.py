import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega a chave
load_dotenv()
chave = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=chave)

print("Procurando modelos liberados para a sua chave...\n")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Modelo disponível: {m.name}")
except Exception as e:
    print(f"Erro ao acessar a API: {e}")