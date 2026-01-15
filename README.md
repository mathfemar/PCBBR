# PCBBR

Sistema de monitoramento e scraping de preços de hardware (Pichau, Terabyte, Kabum, Amazon).

## Estrutura
- **backend/**: API Python (FastAPI).
- **frontend/**: App Flutter (Em desenvolvimento).
- **database/**: Banco de Dados SQLite.

## Como Rodar (Backend)

### Pré-requisitos
- Python 3.10+ instalado.

### Passo a Passo

1.  **Instalar Dependências e Rodar**:
    Execute o arquivo `start_api.bat` na raiz do projeto.

    OU manualmente:
    ```bash
    pip install -r backend/requirements.txt
    cd backend
    python main.py
    ```

2.  **Testar a API**:
    Abra no navegador: [http://localhost:8000/docs](http://localhost:8000/docs)
    Você verá a documentação interativa (Swagger UI).
    
    Exemplo de busca:
    `GET http://localhost:8000/search?url=https://www.terabyteshop.com.br/...`
