# 🌱 Lume — Agente de IA WeNove

> Assistente corporativo inteligente baseado em **RAG (Retrieval-Augmented Generation)**, desenvolvido para apoiar as operações da **WeNove**, um ecossistema de moda circular.

🌐 **Idioma:** 🇧🇷 Português (PT-BR)

---

## 📌 Sobre o Projeto

O **Lume** é um agente de Inteligência Artificial desenvolvido especificamente para a **WeNove**, um ecossistema e marketplace voltado à **moda circular**.

Sua principal função é atuar como um **cérebro operacional**, permitindo que fundadores e membros da equipe consultem informações internas da empresa de forma rápida e natural, utilizando **texto ou voz**.

O agente utiliza uma arquitetura baseada em **RAG (Retrieval-Augmented Generation)** para recuperar informações relevantes de uma base de conhecimento e utilizá-las como contexto para geração das respostas.

Entre os conteúdos que podem ser consultados estão:

* 📄 Regras e documentos internos em `.txt`
* 📊 Tabelas e dados operacionais em `.csv`
* 📚 Base de conhecimento vetorial persistente
* 🎙️ Interações por voz
* 💬 Consultas realizadas diretamente pela interface de chat

O objetivo é fornecer respostas **contextualizadas, fundamentadas e alinhadas ao conhecimento interno da organização**, reduzindo respostas especulativas ou desconectadas da realidade da empresa.

---

## ✨ Principais Funcionalidades

### 🎙️ Interação por Voz e Texto

O Lume permite que o usuário interaja tanto por texto quanto por voz.

* **Speech-to-Text:** `SpeechRecognition`
* **Text-to-Speech:** `gTTS`
* Interface de conversação integrada ao Streamlit

Isso possibilita uma experiência mais acessível e natural para diferentes perfis de usuários.

### 📄 Análise de Arquivos

O sistema permite o envio de arquivos diretamente pela interface, possibilitando análises contextualizadas de:

* `.txt`
* `.csv`

Os arquivos enviados podem ser utilizados como contexto durante a interação com o agente.

### 🎯 Respostas Fundamentadas em Contexto

O Lume foi projetado para reduzir alucinações.

O agente recebe instruções para fundamentar suas respostas prioritariamente nas informações recuperadas da base vetorial ou nos documentos fornecidos pelo usuário.

Quando uma informação não está disponível no contexto fornecido, o sistema pode evitar apresentar uma resposta como se ela fosse um fato conhecido da organização.

### 🧠 RAG com ChromaDB

O sistema utiliza **ChromaDB** como banco de dados vetorial local para armazenar e recuperar os documentos utilizados como conhecimento do agente.

Essa abordagem permite:

* Busca semântica
* Recuperação contextual
* Baixa latência
* Execução local da infraestrutura de embeddings
* Ausência de dependência de um banco vetorial externo

### 🎨 Interface Customizada

Apesar de utilizar Streamlit como framework de interface, o Lume possui uma camada visual personalizada através de **CSS customizado**.

A interface foi desenvolvida buscando manter a identidade visual da WeNove, incluindo:

* Menus flutuantes
* Componentes de interação personalizados
* Organização visual do chat
* Elementos de upload
* Controles relacionados à interação por áudio

---

## 💬 Exemplos de Interação

### 📚 Consulta às Regras de Curadoria

**Usuário:**

> Quais são os critérios para uma peça de roupa ser aceita na nossa curadoria de moda circular?

**Lume:**

> Para ser aceita em nossa plataforma, a peça deve estar limpa, sem rasgos ou manchas permanentes, e pertencer a uma das categorias homologadas pela equipe de curadoria ambiental.
>
> **Fonte consultada:** `regras_curadoria.txt`

---

### 📊 Análise de Dados Dinâmica

**Usuário:**

> *Anexa o arquivo `vendas_agosto.csv`*
>
> Resuma o volume de transações deste arquivo.

**Lume:**

> Analisando a planilha fornecida, o volume total de transações em agosto foi de **142 itens de moda circular**, totalizando um repasse de **R$ 4.350,00** para os vendedores parceiros.

---

## 🛠️ Tecnologias Utilizadas

| Categoria            | Tecnologia                         |
| -------------------- | ---------------------------------- |
| Linguagem            | **Python 3.11**                    |
| Interface Web        | **Streamlit**                      |
| Orquestração         | **LangChain Core**                 |
| Modelo de Linguagem  | **Google Gemini 2.5 Flash**        |
| Banco Vetorial       | **ChromaDB**                       |
| Embeddings           | **HuggingFace — all-MiniLM-L6-v2** |
| Speech-to-Text       | **SpeechRecognition**              |
| Text-to-Speech       | **gTTS**                           |
| Manipulação de Dados | **pandas**                         |
| Customização Visual  | **CSS**                            |

### 🔍 Embeddings Locais

O modelo `all-MiniLM-L6-v2`, disponibilizado através do HuggingFace, é executado localmente.

Isso reduz a dependência de APIs externas para a etapa de geração dos embeddings e evita custos adicionais relacionados a esse processamento.

---

## 🏗️ Arquitetura do Sistema

O Lume utiliza uma arquitetura **RAG**, combinando uma base de conhecimento persistente com documentos enviados dinamicamente durante a utilização do sistema.

```text
                         ┌──────────────────────────────┐
                         │       INPUT DO USUÁRIO       │
                         │                              │
                         │   Texto ou Microfone 🎙️      │
                         └──────────────┬───────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────┐
                         │     PROCESSAMENTO DE ÁUDIO   │
                         │                              │
                         │ SpeechRecognition → Texto    │
                         └──────────────┬───────────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                         ▼                             ▼
              ┌─────────────────────┐       ┌─────────────────────┐
              │ DOCUMENTO ANEXADO   │       │  BASE DE CONHECIMENTO│
              │                     │       │                     │
              │     .txt / .csv     │       │       ChromaDB      │
              └──────────┬──────────┘       └──────────┬──────────┘
                         │                             │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────┐
                         │      LANGCHAIN CORE          │
                         │                              │
                         │   Prompt + Contexto RAG     │
                         │   + Embeddings Locais        │
                         └──────────────┬───────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────┐
                         │     GOOGLE GEMINI 2.5 FLASH  │
                         │                              │
                         │       Geração da Resposta    │
                         └──────────────┬───────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────┐
                         │       SAÍDA MULTIMODAL       │
                         │                              │
                         │    💬 Chat + 🔊 Áudio       │
                         │           via gTTS           │
                         └──────────────────────────────┘
```

---

## 🔄 Fluxo de Funcionamento

De forma simplificada, o processamento segue as seguintes etapas:

1. O usuário envia uma pergunta por **texto ou voz**.
2. Caso seja áudio, o `SpeechRecognition` converte a fala em texto.
3. O sistema identifica o contexto necessário para responder à pergunta.
4. Informações relevantes são recuperadas da **base vetorial ChromaDB**.
5. Caso exista um arquivo anexado, seu conteúdo também pode ser utilizado como contexto.
6. O **LangChain Core** organiza o prompt e o contexto recuperado.
7. O **Google Gemini 2.5 Flash** processa as informações e gera a resposta.
8. A resposta é apresentada na interface do Streamlit.
9. Quando solicitado, o `gTTS` converte a resposta em áudio.

---

## ☁️ Deploy e Infraestrutura

### Decisão de Arquitetura

O escopo acadêmico inicial do projeto previa o provisionamento da aplicação em uma instância de **Compute da Oracle Cloud Infrastructure (OCI)** utilizando contêineres Docker.

Durante a etapa de infraestrutura, entretanto, foram encontrados bloqueios relacionados ao sistema antifraude e ao processo de cadastro da provedora, incluindo restrições relacionadas a cartões e contas universitárias.

Diante desse cenário, a estratégia de deploy foi **adaptada de forma ágil**, priorizando a disponibilidade da aplicação e a validação do produto pela equipe da WeNove.

A aplicação foi então migrada para o:

**Streamlit Community Cloud**

Essa decisão permitiu manter o objetivo principal da entrega:

* ☁️ Aplicação hospedada na nuvem
* 🌎 Acesso remoto
* 🚀 Deploy simplificado
* 🔄 Facilidade de atualização
* ✅ Produto funcional para validação

### 🌐 Aplicação em Produção

**Acesse o Lume:**

[https://lume-agente-ia.streamlit.app/](https://lume-agente-ia.streamlit.app/)

---

## 🚀 Instalação Local

### 1. Clone o repositório

```bash
git clone https://github.com/leonardoferrza/lume-agente-ia.git

cd lume-agente-ia
```

### 2. Crie um ambiente virtual

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

As dependências incluem as bibliotecas necessárias para funcionamento da aplicação, processamento de dados e recursos de áudio.

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GOOGLE_API_KEY="SUA_CHAVE_AQUI"
```

> ⚠️ **Importante:** nunca publique sua chave de API diretamente no código ou no repositório. Utilize variáveis de ambiente e mantenha o arquivo `.env` no `.gitignore`.

### 5. Execute a aplicação

```bash
streamlit run app.py
```

Após iniciar, o Streamlit disponibilizará a aplicação localmente no navegador.

> ℹ️ Na primeira execução, o modelo de embeddings `all-MiniLM-L6-v2` será baixado para o ambiente local.

---

## 📁 Estrutura do Projeto

Uma estrutura esperada para o projeto é:

```text
lume-agente-ia/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── data/
│   ├── regras_curadoria.txt
│   └── ...
│
├── chroma_db/
│   └── ...
│
└── README.md
```

> A estrutura acima pode variar de acordo com a organização atual dos módulos e arquivos do projeto.

---

## 🔐 Segurança

As credenciais utilizadas pela aplicação devem ser armazenadas através de variáveis de ambiente.

Não recomendamos versionar:

```text
.env
```

ou qualquer arquivo contendo:

```text
GOOGLE_API_KEY
```

Adicione o `.env` ao `.gitignore`:

```gitignore
.env
venv/
__pycache__/
chroma_db/
```

---

## 🎯 Objetivos do Projeto

O desenvolvimento do Lume busca demonstrar a aplicação prática de Inteligência Artificial Generativa em um contexto empresarial real.

Entre os principais objetivos estão:

* Aplicar conceitos de **RAG** em um cenário corporativo.
* Criar um assistente baseado no conhecimento interno da empresa.
* Permitir consultas em linguagem natural.
* Integrar interação por voz e texto.
* Realizar análise de dados através de arquivos `.csv`.
* Desenvolver uma interface de usuário personalizada.
* Criar uma solução com infraestrutura simples e de baixo custo.
* Validar uma aplicação de IA com potencial de utilização real pela WeNove.

---

## 🌱 Sobre a WeNove

A **WeNove** é um ecossistema voltado à **moda circular**, buscando conectar tecnologia, sustentabilidade e economia circular.

Dentro desse ecossistema, o Lume funciona como uma camada de **inteligência operacional**, permitindo que informações e processos internos sejam acessados de maneira mais rápida e intuitiva.

---

## 🎓 Contexto Acadêmico

O Lume foi desenvolvido como parte do **Challenge Agente IA**, realizado no contexto da:

**Oracle Next Education (ONE) + Alura**

O projeto explora conceitos de:

* Inteligência Artificial Generativa
* RAG
* LLMs
* Engenharia de Prompts
* Bancos de dados vetoriais
* Embeddings
* Processamento de linguagem natural
* Interfaces conversacionais
* Deploy de aplicações de IA

---

## 👨‍💻 Autor

**Leonardo Ferrza**

Estudante de **Engenharia de Software** e desenvolvedor do projeto Lume.

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e de demonstração.

Consulte os termos de uso e distribuição definidos pelo proprietário do projeto antes de reutilizar ou redistribuir o código.

---

<p align="center">
  🌱 <strong>Lume</strong> — Inteligência para tornar a operação da WeNove mais simples.
</p>
