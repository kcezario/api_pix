# 💸 Pix Backend - Integração com Banco Inter

Este projeto é um backend em Python para realizar pagamentos via Pix utilizando a API oficial do Banco Inter (contas PJ). Ele autentica via OAuth 2.0 com certificado digital e executa pagamentos diretamente para uma chave Pix.

---

## 🚀 Funcionalidades

- 🔐 Autenticação OAuth 2.0 com certificado mTLS
- 💰 Pagamento Pix (chave, valor, descrição)
- ✅ Validação completa dos dados de entrada
- 🔄 Comunicação segura com a API oficial do Banco Inter
- 🧪 Pronto para testes via Swagger
- 🧪 Simulação com `TEST_MODE=true` (sem disparar pagamentos reais)

---

## 🗂️ Estrutura do Projeto

```
pix_backend/
├── app/
│   ├── auth.py           # Autenticação OAuth com certificado
│   ├── config.py         # Configurações (.env)
│   ├── inter_api.py      # Pagamento via API Pix
│   ├── models.py         # Validação da requisição
│   ├── routes.py         # Endpoint HTTP /pagar
│   └── __init__.py
├── main.py               # Inicialização da aplicação
├── .env                  # Variáveis de ambiente (não versionar)
├── .env.example          # Exemplo de .env
├── requirements.txt      # Dependências
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.9+
- Conta PJ no Banco Inter com acesso à API Pix
- Certificado digital da aplicação (.pem + chave)

---

## 📦 Instalação

```bash
# Clonar o projeto
git clone https://github.com/seuusuario/pix-backend.git
cd pix-backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows

# Instalar dependências
pip install -r requirements.txt

# Copiar exemplo de .env e preencher
cp .env.example .env
```

---

## 🧪 Executando em modo desenvolvimento

```bash
uvicorn main:app --reload
```

Acesse:
- `http://localhost:8000` → Health check
- `http://localhost:8000/docs` → Swagger UI para testes

---

## 🧪 Testando com `TEST_MODE=true`

Durante o desenvolvimento ou integração, você pode simular pagamentos **sem executar nenhuma operação real**.

### Como ativar:

No seu `.env`:

```env
TEST_MODE=true
```

### Comportamento:

- Nenhuma requisição será enviada ao Banco Inter
- Você verá mensagens no terminal como:
  ```
  TEST_MODE: Simulando pagamento Pix...
  → key: email@exemplo.com
  → amount: 20.5
  → description: Pagamento de teste
  ```

- A resposta no Swagger será:
```json
{
  "status": "sucesso",
  "data": {
    "status": "simulado",
    "key": "email@exemplo.com",
    "amount": 20.5,
    "description": "Pagamento de teste",
    "message": "Pagamento simulado com sucesso (modo de teste)"
  }
}
```

---

## 🔐 Exemplo de Requisição

```json
POST /pagar
{
  "key": "email@exemplo.com",
  "amount": 20.5,
  "description": "Pagamento de teste"
}
```

---

## 📄 Documentação da API Banco Inter

- [🔗 API Pix - Pagamento](https://developers.inter.co/references/pix#pix-pagamento)
- [🔗 Autenticação OAuth 2.0](https://developers.inter.co/references/authentication)

---

## 🛡️ Aviso de Segurança

- Nunca exponha seu `.env` ou certificados no repositório.
- Certificados têm validade limitada — configure rotação segura.
- Use HTTPS e proteja o backend com autenticação/autorização se for para produção.
