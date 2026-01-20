# Guia de Contribuição - PCBBR

## 📁 Organização do Projeto

### Estrutura Limpa
O projeto está organizado da seguinte forma:

#### Raiz do Projeto
- `catalog_bot.py` - CLI para catalogar produtos
- `start_api.bat` - Script para iniciar apenas a API
- `start_project.bat` - Script para iniciar API + Frontend
- `run_catalog.bat` - Script para executar catalogação
- `requirements.txt` - Dependências Python

#### Backend (`/backend`)
- `main.py` - Servidor FastAPI
- `models.py` - Modelos do banco de dados
- `database.py` - Configuração do SQLite
- `/services` - Lógica de negócio
  - `/scrapers` - Scrapers por loja (kabum, pichau, terabyte, amazon)
- `/alembic` - Migrações do banco de dados

#### Frontend (`/frontend`)
- Aplicação Flutter (em desenvolvimento)

#### Debug (`/debug`)
- **ATENÇÃO:** Arquivos de teste e debug temporários
- Scripts de análise HTML
- Amostras de páginas das lojas
- Testes antigos
- Documentação temporária

## 🔧 Convenções de Código

### Python
- Use `snake_case` para funções e variáveis
- Use `PascalCase` para classes
- Docstrings em todas as funções públicas
- Type hints sempre que possível

### Scrapers
Ao adicionar um novo scraper:
1. Crie arquivo em `backend/services/scrapers/`
2. Implemente as funções padrão:
   - `scrape_product(url)` - Scraping de produto individual
   - `scrape_category(category, max_products)` - Scraping de categoria com paginação
3. Use `curl_cffi` com impersonation Chrome 120
4. Adicione rate limiting (1 segundo entre requests)
5. Implemente detecção de duplicatas com `seen_urls`

### Banco de Dados
- Use SQLModel para models
- Crie migrations Alembic para mudanças no schema
- Nunca delete dados de produção

## 🧪 Testes

Arquivos de teste devem ir para `/debug`:
- Scripts de análise temporários
- Amostras HTML das lojas
- Testes unitários experimentais

## 📝 Commits

Formato recomendado:
```
tipo(escopo): descrição curta

Descrição mais detalhada se necessário
```

Tipos:
- `feat` - Nova funcionalidade
- `fix` - Correção de bug
- `refactor` - Refatoração de código
- `docs` - Documentação
- `test` - Testes
- `chore` - Tarefas de manutenção

Exemplos:
- `feat(scraper): adiciona paginação ao scraper da Kabum`
- `fix(api): corrige timeout em requisições longas`
- `refactor(database): reorganiza estrutura de models`

## 🚀 Workflow de Desenvolvimento

1. Criar branch a partir de `main`
2. Desenvolver e testar localmente
3. Mover arquivos temporários para `/debug`
4. Atualizar documentação se necessário
5. Commit com mensagem descritiva
6. Push e criar Pull Request

## ⚠️ Boas Práticas

### ✅ FAÇA
- Teste scrapers com rate limiting
- Documente mudanças no README
- Use logs para debug (`logging` module)
- Valide dados antes de salvar no banco
- Trate exceções adequadamente

### ❌ NÃO FAÇA
- Commitar arquivos de cache (`__pycache__`)
- Commitar arquivos `.html` ou `.txt` de teste
- Fazer scraping sem rate limiting
- Hardcode URLs ou credenciais
- Deixar `print()` statements no código final

## 📊 Adicionando Nova Categoria

Para adicionar uma nova categoria de produtos:

1. Defina o nome no `catalog_bot.py`
2. Adicione o mapeamento de URL em cada scraper
3. Teste com uma loja primeiro
4. Documente exemplos de produtos

## 🛠️ Tecnologias Principais

- **Backend:** Python 3.10+, FastAPI, SQLModel, Alembic
- **Scraping:** curl_cffi, BeautifulSoup4
- **Frontend:** Flutter (Dart)
- **Database:** SQLite
- **Logging:** Python logging module
