# 📦 Backend Iris - Blog API

Este repositório representa a API backend do projeto Iris dentro de um cluster GKE da Google Cloud, construída com **Flask**, persistência em **PostgreSQL**, e orquestrada com **Docker Compose**.

---

## 🚀 Tecnologias Utilizadas

- Python 3.10 / Flask
- PostgreSQL
- Docker & Docker Compose
- GitHub Actions
- Kubernets

---

## 🌱 Fluxo de Branches

```mermaid
gitGraph
   commit id: "main"
   branch develop
   commit id: "dev commit"
   branch feature/login
   commit id: "login implementado"
   checkout develop
   merge release
   checkout main
   merge develop
```
---

### ⚙️ Estrutura do Pipeline (CI/CD)

Pipeline automatizado com GitHub Actions, disparado em push para a `main` e `develop`.

#### 1. `test`
- Inicia container PostgreSQL
- Configura ambiente virtual Python
- Instala dependências via `requirements.txt`
- Executa:
  - `pytest tests/user_test.py`
  - `pytest tests/comment_test.py`

#### 2. `build`
- Realiza conexão com Google Cloud através de service account
- Atualiza a imagem do artifact registery

#### 3. `deploy`
- Faz deploy no Google Kubernetes Engine no cluster respectivo à branch atualizada. 

#### 4. `Release`
- Caso o push vá para a release será enviado um e-mail para notificar sobre a nova versão. 

---

### 💻 Instruções para rodar localmente

#### 🔧 Requisitos

- Python 3.10+
- Docker e Docker Compose

#### 🔥 Subir com Docker Compose

```bash
docker-compose up --build
```

- O backend estará disponível em: `http://localhost:5000`

---

#### 📦 Executar testes localmente

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
```

---

### 🚢 Deploy em Produção

O deploy é feito automaticamente via **GitHub Actions**, conforme definido em `.github/workflows/main.yml`.

**Etapas:**

1. Merge da branch `develop` para `main`.
2. CI executa:
   -  Testes com Pytest
   -  Build + push da imagem para o Docker Hub
   -  SSH na VM (GCP)
   -  Criação do `.env` com secrets
   -  Parada e remoção do container anterior
   -  Pull da nova imagem
   -  Execução do container com `--env-file .env` e exposto em `5000`


---
