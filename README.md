# PCBBR - Price Comparison Bot Brazil

Sistema de monitoramento e comparação de preços de hardware de lojas brasileiras (Pichau, Terabyte, Kabum).

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)](README.md)

## ✨ Funcionalidades

- 🔍 **Scraping** de produtos das principais lojas brasileiras
- 💾 **Catalogação** automática com paginação
- 🚀 **API REST** com FastAPI
- 📊 **Banco de dados** SQLite com migrações Alembic
- 🔄 **Rate limiting** e detecção de duplicatas
- 🛡️ **Cloudflare bypass** com curl_cffi

## 🏗️ Estrutura do Projeto

```
PCBBR/
├── backend/              # API FastAPI + Scrapers
│   ├── services/        # Lógica de negócio e scrapers
│   │   └── scrapers/   # Scrapers por loja (kabum, pichau, terabyte)
│   ├── alembic/        # Migrações do banco de dados
│   ├── main.py         # Servidor FastAPI
│   ├── models.py       # Modelos SQLModel
│   └── database.py     # Configuração do banco
├── frontend/            # App Flutter (Em desenvolvimento)
├── database/            # Banco SQLite
├── logs/                # Logs do sistema
├── debug/               # Arquivos de teste e debug
├── catalog_bot.py       # CLI para catalogar produtos
├── start_api.bat        # Inicia a API
└── start_project.bat    # Inicia API + Frontend
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- **Python 3.10 ou superior** ([Download aqui](https://www.python.org/downloads/))
  - ⚠️ Durante a instalação, marque "Add Python to PATH"
- **Git** (opcional, para clonar o repositório)
- **Flutter SDK** (apenas se for usar o frontend)

### Primeira Instalação (Windows)

1. **Clone ou baixe o repositório**
   ```bash
   git clone https://github.com/seu-usuario/PCBBR.git
   cd PCBBR
   ```

2. **Execute o setup automático**
   ```bash
   setup.bat
   ```
   
   Este script irá:
   - ✅ Verificar instalação do Python
   - ✅ Criar ambiente virtual (.venv)
   - ✅ Instalar todas as dependências
   - ✅ Criar diretórios necessários

### Linux/Mac

```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r backend/requirements.txt
pip install -r requirements.txt

# Criar diretórios
mkdir -p database logs
```

## 🏃 Como Rodar

### Opção 1: Apenas API (Recomendado para testes)
```bash
start_api.bat
```
A API estará disponível em:
- http://localhost:8000
- Documentação: http://localhost:8000/docs

### Opção 2: API + Frontend (Requer Flutter)
```bash
start_project.bat
```

### Opção 3: Manual
```bash
# Ativar ambiente virtual
.venv\Scripts\activate.bat  # Windows
source .venv/bin/activate   # Linux/Mac

# Rodar API
cd backend
python main.py
```

## 📊 Catalogar Produtos

Use o CLI `catalog_bot.py` para popular o banco de dados:

```bash
# Opção 1: Usar o script (mais fácil)
run_catalog.bat

# Opção 2: Comando direto
python catalog_bot.py --category "CPU"

# Catalogar de uma loja específica
python catalog_bot.py --category "CPU" --store kabum

# Com argumentos personalizados via script
run_catalog.bat --category "Placa de Vídeo" --store pichau
```

### Categorias disponíveis
- CPU
- Placa de Vídeo
- Placa Mãe
- Memória RAM
- SSD
- Fonte

### Lojas suportadas
- **Kabum** - Scraping via JSON do Next.js
- **Pichau** - Scraping com paginação ?page=N
- **Terabyte** - Scraping com paginação ?page=N

## 🔍 Testar a API

Abra no navegador: http://localhost:8000/docs

Endpoints disponíveis:
- `GET /search?url={product_url}` - Buscar preço de produto específico
- `GET /products` - Listar produtos catalogados
- Mais endpoints na documentação Swagger

## 🆘 Problemas?

1. **Verificar compatibilidade:**
   ```bash
   python check_python.py
   ```

2. **Verificar sistema:**
   ```bash
   check_system.bat  # Windows
   ```

3. **Consultar documentação:**
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Soluções para problemas comuns
   - [CONTRIBUTING.md](CONTRIBUTING.md) - Guia de desenvolvimento

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) antes de começar.

## 📜 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 🎯 Roadmap

- [x] Scraping de 3 lojas com paginação
- [x] Catalogação automática de produtos
- [x] API REST funcional
- [ ] Frontend Flutter completo
- [ ] Sistema de notificações de preço
- [ ] Histórico de preços
- [ ] Comparação de preços entre lojas
- [ ] API pública com autenticação
