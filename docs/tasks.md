## 🏁 **Sprint Única: Backend Python com Pagamento Pix via API Banco Inter**

---

### 🔹 **ETAPA 0: Setup Inicial (Ambiente de Desenvolvimento)**

| Task | Descrição |OK|
|------|-----------|--|
| 0.1 | Criar repositório Git (local ou GitHub) | OK |
| 0.2 | Configurar ambiente virtual com `venv` | OK |
| 0.3 | Criar e preencher `requirements.txt` | OK |
| 0.4 | Criar estrutura de pastas base (`app/`, `certs/`, etc.) | OK |
| 0.5 | Adicionar `.gitignore` e `.env.example` com variáveis de ambiente | OK |

---

### 🔹 **ETAPA 1: Autenticação com a API do Banco Inter**

| Task | Descrição |OK|
|------|-----------|--|
| 1.1 | Estudar documentação da rota `/oauth/v2/token` |OK|
| 1.2 | Converter certificado `.pfx` para `.pem`, se necessário |
| 1.3 | Criar `config.py` para carregar variáveis do `.env` |
| 1.4 | Implementar função `get_access_token()` com certificado |
| 1.5 | Testar autenticação e validar retorno do token |

---

### 🔹 **ETAPA 2: Implementar Pagamento Pix (POST /pix/payments)**

| Task | Descrição |
|------|-----------|
| 2.1 | Estudar documentação da rota de pagamento Pix |
| 2.2 | Criar função `efetuar_pagamento_pix()` com headers, payload e cert |
| 2.3 | Criar função para gerar `txid` (UUID com corte de 35 chars) |
| 2.4 | Criar função `main.py` para testar um pagamento de R$10 |
| 2.5 | Testar retorno da API e tratar erros básicos (print/log) |

---

### 🔹 **ETAPA 3: Consultar Status do Pagamento**

| Task | Descrição |
|------|-----------|
| 3.1 | Estudar rota `GET /pix/payments/{txid}` |
| 3.2 | Criar função `consultar_pagamento()` |
| 3.3 | Adicionar chamada no `main.py` para consultar status logo após pagamento |
| 3.4 | Tratar possíveis erros (pagamento não encontrado, etc.) |

---

### 🔹 **ETAPA 4: Organização e Segurança**

| Task | Descrição |
|------|-----------|
| 4.1 | Escrever `.env` com variáveis seguras |
| 4.2 | Criar `.env.example` para facilitar deploy |
| 4.3 | Adicionar tratamento de erros mais robusto (try/except/logs) |
| 4.4 | Garantir que certificados **NÃO** estejam versionados (via `.gitignore`) |

---

### 🔹 **ETAPA 5: Opcional – API REST com FastAPI (ou Flask)**

> Caso queira expor como uma API.

| Task | Descrição |
|------|-----------|
| 5.1 | Instalar FastAPI e Uvicorn |
| 5.2 | Criar endpoint `POST /pix/pagamento` |
| 5.3 | Criar endpoint `GET /pix/status/{txid}` |
| 5.4 | Testar com Postman ou cURL |
| 5.5 | Adicionar validações de entrada com Pydantic |

---

### 🔹 **ETAPA 6: Entrega Final / Validação**

| Task | Descrição |
|------|-----------|
| 6.1 | Testar com valores reais em homologação |
| 6.2 | Verificar logs e retornos em diferentes cenários |
| 6.3 | Gerar documentação mínima (README com uso básico) |
| 6.4 | Validar com a equipe responsável pela parte financeira |

---

## ✅ **Checklist Geral**

- [ ] Projeto criado com estrutura limpa
- [ ] Variáveis sensíveis isoladas no `.env`
- [ ] Autenticação via certificado funcionando
- [ ] Pagamento Pix sendo enviado com sucesso
- [ ] Consulta de status funcionando
- [ ] Código limpo e com tratamento de erros básico
- [ ] (Opcional) API REST criada com FastAPI
- [ ] Projeto documentado para uso interno

---

Se quiser, posso gerar isso como uma board em formato Markdown para copiar pro GitHub Projects ou Notion. Também posso te ajudar a fazer deploy disso numa VPS ou Docker. Quer?