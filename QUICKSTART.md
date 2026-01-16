# 🚀 Guia Rápido de Início - PCBBR

## Para Usuários (Apenas usar o projeto)

### Windows

```bash
# 1. Baixar o projeto
git clone https://github.com/seu-usuario/PCBBR.git
cd PCBBR

# 2. Verificar Python (opcional mas recomendado)
python check_python.py

# 3. Instalar tudo automaticamente
setup.bat

# 4. Iniciar API
start_api.bat

# 5. Testar no navegador
# Abra: http://localhost:8000/docs
```

### Linux/Mac

```bash
# 1. Baixar o projeto
git clone https://github.com/seu-usuario/PCBBR.git
cd PCBBR

# 2. Verificar Python (opcional)
python3 check_python.py

# 3. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 4. Instalar dependências
pip install -r backend/requirements.txt
pip install -r requirements.txt

# 5. Criar diretórios
mkdir -p database logs

# 6. Iniciar API
cd backend
python main.py
```

---

## Para Desenvolvedores

### Configuração Inicial

```bash
# 1. Clone e setup
git clone https://github.com/seu-usuario/PCBBR.git
cd PCBBR
setup.bat  # Windows

# 2. Verificar se tudo está OK
check_system.bat  # Windows
python check_python.py  # Linux/Mac

# 3. Iniciar em modo desenvolvimento
start_api.bat
```

### Catalogar Produtos

```bash
# Catalogar CPUs de todas as lojas
python catalog_bot.py --category "CPU"

# Catalogar de uma loja específica
python catalog_bot.py --category "Placa de Vídeo" --store kabum

# Usar o script auxiliar
run_catalog.bat --category "CPU" --store pichau
```

### Estrutura de Desenvolvimento

```python
# Adicionar novo scraper
backend/services/scrapers/nova_loja.py

def scrape_product(url: str) -> dict:
    """Scraping de produto individual"""
    pass

def scrape_category(category: str, max_products: int = 500) -> List[dict]:
    """Scraping de categoria com paginação"""
    pass
```

### Testes

```bash
# Scripts de teste estão em /debug
cd debug
python test_scrapers.py
```

### Contribuir

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m "feat: adiciona nova funcionalidade"`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

Leia [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

---

## Comandos Úteis

### Gerenciar Ambiente Virtual

```bash
# Ativar
.venv\Scripts\activate.bat  # Windows
source .venv/bin/activate   # Linux/Mac

# Desativar
deactivate

# Recriar do zero
rmdir /s .venv  # Windows
rm -rf .venv    # Linux/Mac
setup.bat       # Windows
python -m venv .venv && source .venv/bin/activate  # Linux/Mac
```

### API

```bash
# Iniciar
start_api.bat  # Windows
python backend/main.py  # Linux/Mac

# Ver docs
http://localhost:8000/docs

# Testar endpoint
curl http://localhost:8000/products
```

### Banco de Dados

```bash
# Ver produtos catalogados
sqlite3 database/database.db "SELECT COUNT(*) FROM product;"

# Limpar banco (cuidado!)
del database\database.db  # Windows
rm database/database.db   # Linux/Mac
```

---

## Atalhos

| Comando | Descrição |
|---------|-----------|
| `setup.bat` | Configuração inicial completa |
| `start_api.bat` | Inicia apenas a API |
| `run_catalog.bat` | Cataloga produtos |
| `check_system.bat` | Verifica se tudo está OK |
| `python check_python.py` | Verifica Python |

---

## Precisa de Ajuda?

- 📖 [README.md](README.md) - Documentação completa
- 🐛 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Soluções de problemas
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - Guia de desenvolvimento
- 💬 Abra uma issue no GitHub

---

## Checklist de Instalação

- [ ] Python 3.10+ instalado
- [ ] `python check_python.py` passa
- [ ] `setup.bat` executado sem erros
- [ ] `start_api.bat` funciona
- [ ] http://localhost:8000/docs abre
- [ ] `catalog_bot.py` cataloga produtos

✅ Tudo pronto? Comece a usar!
