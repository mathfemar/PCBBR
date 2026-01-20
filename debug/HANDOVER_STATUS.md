# PCBBR - Status do Projeto & Handover 🚀

Este documento serve como um **checkpoint detalhado** para continuar o desenvolvimento em outro ambiente. Ele contextualiza o estado atual do código, da arquitetura e os próximos passos imediatos.

---

## 1. Visão Geral
O projeto é um **Agregador de Preços de Hardware** focado no mercado brasileiro (Pichau, Terabyte, Kabum, Amazon).
*   **Arquitetura**: Backend em Python (FastAPI) + Frontend em Flutter (Clean Architecture).
*   **Objetivo Atual**: O Backend está 100% funcional. O Frontend precisa ser iniciado.

## 2. O Que Está Pronto (Backend) ✅
Todo o código Python está na pasta `backend/`.

### A. Scrapers (`backend/services/scrapers/`)
Implementamos 4 scrapers robustos usando `curl_cffi` (para bypass de Cloudflare) e `BeautifulSoup`.
*   **Amazon**: CSS Selectors (`.a-price .a-offscreen`).
*   **Kabum**: API Oculta (`__NEXT_DATA__`).
*   **Pichau**: Meta Tags (robusto contra mudanças de layout).
*   **Terabyte**: JSON-LD.
*   *Nota*: SSL Verification foi desabilitada (`verify=False`) para contornar proxies corporativos. Pode ser reativado em casa.

### B. API (`backend/main.py`)
Servidor **FastAPI** rodando na porta `8000`.
*   **Endpoint Principal**: `GET /search?url=...`
*   **Lógica**: Recebe a URL -> Identifica a Loja -> Roda o Scraper -> **Salva no Banco** -> Retorna JSON.

### C. Banco de Dados (`backend/database.py`, `models.py`)
Utilizamos **SQLModel** (SQLAlchemy + Pydantic) com **SQLite**.
*   **Arquivo**: `database/pcbbr.db` (Já migrado e funcional).
*   **Tabelas**:
    *   `Product`: Dados cadastrais e último preço (Cache).
    *   `PriceHistory`: Histórico completo de preços por timestamp.
*   **Migrations**: Gerenciadas pelo **Alembic** (`backend/alembic/`).

### D. Persistência (`backend/services/product_service.py`)
A lógica de "Upsert" está pronta. Se o produto existe, atualiza o preço; se mudou, cria novo histórico.

---

## 3. O Que Falta (Frontend) 🚧
O projeto Flutter **ainda não foi criado** porque o executável `flutter` não estava disponível no PATH deste ambiente.

### Estrutura Planejada (`frontend/`)
A pasta `frontend/` existe mas contém apenas um `pubspec.yaml` rascunho. O objetivo é usar **Clean Architecture**.

**Dependências Desejadas:**
*   `flutter_riverpod` (Estado)
*   `dio` (HTTP)
*   `go_router` (Rotas)

---

## 4. Como Continuar (Passo a Passo)

### Passo 1: Setup do Backend (No novo PC)
1.  Clone o repositório.
2.  Crie um venv: `python -m venv .venv`.
3.  Instale deps: `pip install -r backend/requirements.txt`.
4.  Rode a API:
    ```bash
    cd backend
    python main.py
    # Ou use o start_api.bat na raiz
    ```
5.  Teste acessando: `http://localhost:8000/docs`.

### Passo 2: Criar o Frontend (Ação Principal) ⚡
Como o projeto Flutter não existe, você deve criá-lo **sobrescrevendo** a pasta frontend atual.

No terminal (na raiz do projeto):
```bash
# 1. Apague a pasta frontend atual (que só tem o pubspec) ou mova o pubspec.yaml para backup.
# 2. Crie o projeto oficial:
flutter create --org com.pcbbr --project-name pcbbr_app frontend

# 3. Adicione as dependências (Riverpod, Dio, etc.)
cd frontend
flutter pub add flutter_riverpod dio go_router google_fonts intl url_launcher
```

### Passo 3: Implementar a UI
Peça para o agente de IA:
*"Crie a estrutura de pastas Clean Architecture dentro de `frontend/lib` e implemente uma tela de busca simples que consome `http://localhost:8000/search`."*

---

## 5. Árvore de Arquivos Importantes
```text
PCBBR/
├── database/pcbbr.db           # Banco SQLite (Git Tracked por enquanto)
├── backend/
│   ├── main.py                 # API Entrypoint
│   ├── database.py             # Conexão DB
│   ├── models.py               # Tabelas SQLModel
│   └── services/
│       ├── product_service.py  # Lógica de Salvar no Banco
│       └── scrapers/           # Scripts de cada loja (amazon.py, etc)
└── frontend/                   # (A SER CRIADO PELO FLUTTER)
```

**Boa sorte! O Backend está sólido como uma rocha. Foque 100% no Flutter agora.** 🦅
