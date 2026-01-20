# Solução de Problemas - PCBBR

## 🐛 Problemas Comuns e Soluções

### ❌ "Python não encontrado" ou "python is not recognized"

**Causa:** Python não está instalado ou não está no PATH.

**Solução:**
1. Baixe Python 3.10+ de: https://www.python.org/downloads/
2. Durante a instalação, **marque a opção "Add Python to PATH"**
3. Reinicie o terminal/computador
4. Teste com: `python --version`

---

### ❌ "pip is not recognized"

**Causa:** pip não está no PATH (raro se Python foi instalado corretamente).

**Solução:**
```bash
# Usar python -m pip ao invés de pip
python -m pip install -r requirements.txt
```

---

### ❌ Erro ao criar ambiente virtual (.venv)

**Causa:** Módulo venv não instalado ou corrompido.

**Solução:**
```bash
# Windows
python -m pip install --upgrade pip
python -m venv .venv --clear

# Linux/Mac
python3 -m pip install --upgrade pip
python3 -m venv .venv --clear
```

---

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

**Causa:** Dependências não instaladas ou ambiente virtual não ativado.

**Solução:**
```bash
# 1. Ativar ambiente virtual
.venv\Scripts\activate.bat  # Windows
source .venv/bin/activate   # Linux/Mac

# 2. Instalar dependências
pip install -r backend/requirements.txt
```

---

### ❌ Erro "curl_cffi" em instalação

**Causa:** curl_cffi requer compiladores C++ em alguns sistemas.

**Solução Windows:**
1. Instale Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
2. Ou use versão pré-compilada:
   ```bash
   pip install curl_cffi --only-binary=:all:
   ```

**Solução Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install build-essential python3-dev

# Fedora
sudo dnf install gcc python3-devel
```

---

### ❌ API não inicia - Porta 8000 já em uso

**Causa:** Outra aplicação está usando a porta 8000.

**Solução 1:** Feche a aplicação que está usando a porta
```bash
# Windows - Ver processos na porta 8000
netstat -ano | findstr :8000

# Matar processo (substitua PID pelo número encontrado)
taskkill /PID [PID] /F
```

**Solução 2:** Mude a porta no `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Porta 8001 ao invés de 8000
```

---

### ❌ Erro de encoding ao catalogar produtos

**Causa:** Terminal não suporta UTF-8.

**Solução:**
O script `catalog_bot.py` já tem tratamento, mas se persistir:
```bash
# Windows - Force UTF-8
chcp 65001
python catalog_bot.py --category "CPU"
```

---

### ❌ Banco de dados travado - "database is locked"

**Causa:** Múltiplas instâncias acessando o banco simultaneamente.

**Solução:**
1. Feche todas as instâncias do catalog_bot e API
2. Delete o arquivo `database/database.db-journal` (se existir)
3. Inicie apenas uma instância por vez

---

### ❌ Scrapers retornam 0 produtos

**Possíveis causas:**
1. Loja mudou estrutura HTML
2. Cloudflare bloqueou requisição
3. Categoria não existe na loja

**Solução:**
1. Teste com categoria diferente: `--category "CPU"`
2. Verifique os logs em `logs/`
3. Teste uma loja específica: `--store kabum`
4. Verifique se curl_cffi está atualizado: `pip install --upgrade curl_cffi`

---

### ❌ Erro "Permission denied" ao criar diretórios

**Causa:** Sem permissões no diretório.

**Solução:**
```bash
# Windows - Execute como Administrador
# Clique direito no arquivo .bat > "Executar como administrador"

# Linux/Mac
sudo python catalog_bot.py --category "CPU"
# Ou mude permissões da pasta
chmod -R 755 .
```

---

### ❌ Frontend Flutter não compila

**Causa:** SDK Flutter não instalado ou desatualizado.

**Solução:**
O projeto foi desenhado para funcionar **sem o frontend**. Use apenas a API:
```bash
start_api.bat
```

Se quiser o frontend:
1. Instale Flutter: https://docs.flutter.dev/get-started/install
2. `flutter doctor` para verificar setup
3. `flutter pub get` na pasta frontend/

---

### ❌ Git bash não reconhece .bat files

**Causa:** Git bash é um shell Unix-like, arquivos .bat são Windows.

**Solução:**
Use PowerShell ou CMD no Windows:
```bash
# PowerShell/CMD
setup.bat
start_api.bat

# Ou use Python diretamente no Git Bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r backend/requirements.txt
cd backend && python main.py
```

---

## 📝 Logs e Debug

### Ver logs do sistema
```bash
# Logs da API e scrapers
cd logs
dir  # Windows
ls   # Linux/Mac
```

### Modo debug
Edite `catalog_bot.py` e adicione:
```python
logging.basicConfig(level=logging.DEBUG)
```

---

## 🆘 Ainda com problemas?

1. Verifique os logs em `logs/`
2. Execute `python --version` e `pip --version`
3. Verifique se `.venv` foi criado corretamente
4. Tente deletar `.venv` e executar `setup.bat` novamente
5. Abra uma issue no GitHub com:
   - Sistema operacional
   - Versão do Python
   - Mensagem de erro completa
   - Comandos executados

---

## ✅ Checklist de Instalação Bem-Sucedida

- [ ] Python 3.10+ instalado e no PATH
- [ ] `setup.bat` executado sem erros
- [ ] Pasta `.venv` criada
- [ ] `start_api.bat` inicia servidor em http://localhost:8000
- [ ] Acesso a http://localhost:8000/docs funciona
- [ ] `catalog_bot.py` cataloga produtos sem erros
- [ ] Banco `database/database.db` foi criado

Se todos os itens estão marcados, o projeto está funcionando! 🎉
