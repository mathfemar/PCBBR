# 🛒 PCBBR - Status dos Scrapers

Este documento rastreia o progresso no desenvolvimento dos scrapers para as lojas de hardware brasileiras.

## 📊 Status Geral

| Loja | Status | Método Identificado | Dificuldade |
| :--- | :--- | :--- | :--- |
| **TerabyteShop** | ✅ **Pronto** (Validado) | `curl_cffi` + `JSON-LD` | Média (Cloudflare) |
| **Pichau** | ✅ **Pronto** | `curl_cffi` + `Meta Tags` | Média (Cloudflare) |
| **Kabum** | ✅ **Pronto** | `curl_cffi` + `Next.js Data` | Média |
| **Amazon** | ✅ **Pronto** | `curl_cffi` + `CSS Selectors` | Alta |

---

## 🛠️ Detalhes Técnicos e Estratégia

### 1. TerabyteShop
- **Desafio**: Protegido por Cloudflare (dificulta requests normais do Python).
- **Solução**: Uso da biblioteca `curl_cffi` para simular um navegador Chrome real e passar despercebido.
- **Extração**: A página contém dados estruturados em JSON-LD (formato padronizado pelo Google), o que torna a extração do preço e nome muito confiável e menos propensa a quebrar se o design do site mudar.

### 2. Pichau
- **Descoberta**: O print enviado confirma que o site utiliza **Next.js** (vimos o header `Link` apontando para `_next/static`) e é protegido pela **Cloudflare**.
- **Estratégia**:
  - Como é Next.js, os dados do produto (preço, estoque) geralmente vêm embutidos no HTML dentro de uma tag `<script id="__NEXT_DATA__" type="application/json">`.
  - Isso facilita _muito_: basta baixar o HTML com `curl_cffi` e ler esse JSON, sem precisar fazer várias chamadas de API.

### 3. Kabum
- **Estratégia Prevista**:
  - O site da Kabum é feito em Next.js. Frequentemente, os dados do produto estão escondidos em um JSON grande dentro do HTML (`__NEXT_DATA__`) ou acessíveis via API pública não documentada.
  - Faremos engenharia reversa para encontrar o caminho mais limpo.

### 4. Amazon
- **Estratégia Prevista**:
  - A Amazon é conhecida por ter sistemas anti-bot agressivos e layouts que mudam (A/B testing).
  - Uso provável de `seletores CSS` robustos para pegar o preço.
  - Pode exigir rotação de User-Agents ou headers mais complexos.
  - *Fallback*: Se o bloqueio for forte, podemos precisar de bibliotecas como `selenium-driverless` ou proxies (mas tentaremos manter simples primeiro).

---
## 📝 Próximos Passos
1. Finalizar e salvar o script limpo da **Terabyte**.
2. Investigar a **Pichau** (analisar requests de rede).
3. Investigar a **Kabum**.
4. Investigar a **Amazon**.
