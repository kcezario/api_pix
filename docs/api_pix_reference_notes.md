## 🔐 Autenticação OAuth 2.0 - Banco Inter

### ✉️ Endpoint
```
POST https://cdpj.partners.bancointer.com.br/oauth/v2/token
```

### ✉️ Headers obrigatórios
```http
Content-Type: application/x-www-form-urlencoded
```

### ✉️ Corpo da requisição (form-urlencoded)
| Campo           | Tipo     | Obrigatório | Descrição                                                                 |
|------------------|----------|-------------|------------------------------------------------------------------------------|
| `client_id`      | string   | Sim         | Obtido na tela de aplicações do Internet Banking PJ                      |
| `client_secret`  | string   | Sim         | Obtido junto com o client_id                                                |
| `grant_type`     | string   | Sim         | Sempre "client_credentials"                                                 |
| `scope`          | string   | Sim         | Deve incluir `pagamento-pix.write`. Vários escopos separados por espaço.     |

### ⌛ Tempo de validade do token
- 1 hora (3600 segundos)

### ⏳ Rate Limit
- 5 chamadas por minuto

---

## 💳 Pagamento Pix

### 🔗 Endpoint
```
POST https://cdpj.partners.bancointer.com.br/banking/v2/pix
```

### ⚡ Escopo requerido
- `pagamento-pix.write`

### ⏳ Rate Limit
- 60 chamadas por minuto (limitado a 1 por segundo)
- 10 chamadas por minuto (limite de burst)

### 🔑 Headers obrigatórios

| Header               | Tipo     | Obrigatório | Descrição                                                                 |
|----------------------|----------|-------------|------------------------------------------------------------------------------|
| `Authorization`      | string   | Sim         | "Bearer {access_token}" gerado via autenticação OAuth                     |
| `x-id-idempotente`   | UUID     | Sim         | ID único para garantir que pagamentos duplicados não ocorram               |
| `x-conta-corrente`   | string   | Condicional | Apenas se a aplicação estiver vinculada a múltiplas contas correntes       |
| `Content-Type`       | string   | Sim         | "application/json"                                                          |

### 📂 Corpo da requisição (JSON)
Formato para pagamento com **chave Pix**:

```json
{
  "valor": "100.00",
  "descricao": "pagamento...",
  "destinatario": {
    "tipo": "CHAVE",
    "chave": "<chave pix de quem receberá o pagamento>"
  }
}
```

| Campo             | Tipo    | Obrigatório | Descrição                                                                 |
|-------------------|---------|-------------|------------------------------------------------------------------------------|
| `valor`           | string  | Sim         | Valor do pagamento em formato decimal string (ex: "100.00")                 |
| `descricao`       | string  | Não         | Texto opcional (até 140 caracteres)                                          |
| `destinatario`    | objeto  | Sim         | Contém `tipo` e `chave`                                                      |
| `destinatario.tipo` | string | Sim         | Sempre "CHAVE" para este tipo de operação                                    |
| `destinatario.chave`| string | Sim         | Chave Pix do recebedor (email, CPF, CNPJ, EVP, telefone)                    |

### 🚀 Respostas esperadas

**200 OK** - Pagamento realizado com sucesso
```json
{
  "tipoRetorno": "APROVACAO",
  "codigoSolicitacao": "uuid",
  "dataPagamento": "2025-03-27",
  "dataOperacao": "2025-03-27"
}
```

| Campo              | Tipo    | Descrição                                             |
|--------------------|---------|----------------------------------------------------------|
| `tipoRetorno`      | string  | "APROVACAO", "PROCESSADO" ou "AGENDADO"                |
| `codigoSolicitacao`| string  | ID único da solicitação de pagamento                   |
| `dataPagamento`    | string  | Data em que o pagamento está agendado ou foi efetuado   |
| `dataOperacao`     | string  | Data em que o pagamento foi solicitado                   |

### ❌ Erros comuns

- `401 Unauthorized` → token inválido, credenciais erradas ou certificado incorreto
- `403 Forbidden` → escopo incorreto ou não autorizado (`"Faltando escopos necessários"`)
- `422` ou `400` → corpo da requisição malformado
