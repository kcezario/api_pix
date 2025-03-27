# Pix Backend - Integração com Banco Inter

Este projeto é um backend em Python para realizar pagamentos via Pix utilizando a **API oficial do Banco Inter (contas PJ)**.  
A autenticação é feita via OAuth 2.0 com certificado digital e os pagamentos são realizados diretamente para uma **chave Pix**.

---

## Funcionalidades

- Autenticação OAuth 2.0 com certificado mTLS
- Pagamento Pix via chave (CPF, CNPJ, e-mail, telefone ou EVP)
- Validação completa dos dados de entrada com Pydantic
- Modo de simulação com `TEST_MODE=true` (sem enviar Pix real)
- Pronto para testes com Swagger UI

---

## Estrutura do Projeto

```
api_pix/
├── app/
│   ├── auth.py           # Autenticação OAuth com certificado e escopo
│   ├── config.py         # Configurações via .env
│   ├── inter_api.py      # Função principal de pagamento
│   ├── models.py         # Validação de entrada
│   ├── routes.py         # Endpoint POST /pagar
│   └── __init__.py
├── main.py               # Inicialização do FastAPI
├── .env                  # Arquivo com variáveis de ambiente (não versionar)
├── .env.example          # Exemplo de .env
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo :)
```

---

## Requisitos

- Python 3.9+
- Conta **PJ** no Banco Inter com acesso à API Pix
- Certificado da aplicação (`.crt` e `.key`, ou `.pfx` convertido)
- Aplicação criada no Internet Banking com o **escopo `pagamento-pix.write`**

---

## Instalação

```bash
# Clonar o projeto
git clone https://github.com/kcezario/api_pix.git
cd api_pix

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows

# Instalar dependências
pip install -r requirements.txt

# Copiar exemplo de .env e preencher
cp .env.example .env
```

---

## Executando em modo desenvolvimento

```bash
uvicorn main:app --reload
```

Acesse:

- [`http://localhost:8000`](http://localhost:8000) → Health check  
- [`http://localhost:8000/docs`](http://localhost:8000/docs) → Swagger UI para testes

---

## Testando com `TEST_MODE=true`

Durante o desenvolvimento ou integração, você pode simular pagamentos **sem enviar dados reais para o Banco Inter**.

### Como ativar:

```env
TEST_MODE=true
```

### Comportamento:

- Nenhuma requisição real será enviada.
- O terminal mostrará:

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

## Exemplo de Requisição Real

```json
POST /pagar
{
  "key": "11845885000146",
  "amount": 1.00,
  "description": "Teste Pix para CNPJ"
}
```

A resposta será algo como:

```json
{
  "status": "sucesso",
  "data": {
    "tipoRetorno": "APROVACAO",
    "codigoSolicitacao": "UUID...",
    "dataPagamento": "2025-03-27",
    "dataOperacao": "2025-03-27"
  }
}
```

---

## Erros comuns

### 401 Unauthorized

- Verifique `CLIENT_ID`, `CLIENT_SECRET` e os certificados.
- Verifique se a aplicação no Inter é a mesma usada para gerar o certificado.

### 403 Forbidden + `"message": "Faltando escopos necessários."`

- **Solução:** refaça a aplicação no Internet Banking e marque o escopo `pagamento-pix.write`.

---

## Documentação Oficial Banco Inter

- [API Pix - Pagamento](https://developers.inter.co/references/pix#pix-pagamento)
- [Autenticação OAuth 2.0](https://developers.inter.co/references/authentication)
- [Ajuda - Como cadastrar uma API?](https://ajuda.inter.co/conta-digital-pessoa-juridica/como-cadastrar-uma-api)

