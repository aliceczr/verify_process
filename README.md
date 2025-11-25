# 🚀 verify_process

Projeto RAG (Retrieval-Augmented Generation) para verificação/triagem de processos.

Este repositório contém:

- `ml/` — API (FastAPI) com pipeline RAG (Groq + embeddings + FAISS).
- `front/` — interface (Streamlit) opcional.

Este README foca em uma maneira clara, segura e reproduzível de executar o sistema: via Docker.

---

## 🎯 Objetivo

Fornecer uma API que recebe um texto (processo) e retorna uma classificação/justificativa baseada nos documentos indexados.

---

## 🐳 Execução recomendada — somente via Docker

As instruções abaixo permitem executar toda a aplicação sem instalar dependências locais. Isso garante que o ambiente seja igual ao de produção.

### 1️⃣ Pré-requisitos

- **Docker**: Certifique-se de que o Docker está instalado. [Guia de instalação](https://docs.docker.com/get-docker/)
- **Docker Compose**: Incluído na maioria das instalações do Docker.

### 2️⃣ Configuração do ambiente

1. Copie o arquivo `.env.example` para `.env`:

   ```bash
   cp .env.example .env
   ```

2. Preencha as variáveis de ambiente no arquivo `.env` com os valores apropriados.

### 3️⃣ Construção e execução dos containers

1. Para construir e iniciar os serviços (API e interface):

   ```bash
   docker-compose up --build
   ```

2. Acesse os serviços:
   - **API**: [http://localhost:8000](http://localhost:8000)
   - **Interface (opcional)**: [http://localhost:8501](http://localhost:8501)

### 4️⃣ Parar os serviços

Para parar os containers, use:

```bash
docker-compose down
```

---

## 🛠️ Estrutura do Projeto

- **`ml/`**: Contém a lógica principal do pipeline RAG, incluindo:
  - `main.py`: Ponto de entrada da API.
  - `utils.py`: Funções auxiliares.
  - `generate_openapi.py`: Geração automática da documentação OpenAPI.
- **`front/`**: Interface desenvolvida com Streamlit.
- **`knowledge_base/`**: Base de conhecimento.
- **vector_store**: Base de conhecimento indexada

---

## 🧪 Testes

Para rodar os testes (se aplicável), utilize:

```bash
docker exec -it <nome_do_container> pytest
```

---

## 📬 Contato

Para dúvidas ou mais informações:
- **Nome**: Alice Cruz
- **Email**: alicecruz2003@gmail.com

---



