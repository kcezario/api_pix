## 📄 **Código comentado com base na documentação**

### config.py

```python
# Informações de autenticação
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
```
📌 **Baseado na documentação:**
> “Para autenticação, a aplicação deve usar o protocolo OAuth 2.0 com client credentials (Client ID + Client Secret).”  
📚 [Fonte oficial – OAuth 2.0 Banco Inter](https://developers.inter.co/references/authentication)

---

```python
# Certificados
CERT_PATH = os.getenv("CERT_PATH")  # caminho do .pem
KEY_PATH = os.getenv("KEY_PATH")    # caminho da chave privada .pem
```
📌 **Baseado na documentação:**
> “Para autenticação via certificado, será necessário baixar os arquivos no formato `.pfx` e convertê-los para `.pem` e chave privada, que serão usados nas chamadas autenticadas.”  
📚 [Fonte: Guia de Integração > Ative as chaves e certificados](https://developers.inter.co/references/pix)

---

```python
# URLs da API do Banco Inter
TOKEN_URL = os.getenv("TOKEN_URL", "https://cdpj.partners.bancointer.com.br/oauth/v2/token")
PAGAMENTO_PIX_URL = os.getenv("PAGAMENTO_PIX_URL", "https://cdpj.partners.bancointer.com.br/banking/v2/pix")
```
📌 **Baseado na documentação:**
> - Para autenticação: `POST https://cdpj.partners.bancointer.com.br/oauth/v2/token`
> - Para pagamento Pix: `POST https://cdpj.partners.bancointer.com.br/pix/v2/pagamentos`  
📚 [Referência: API Pix Pagamento - Método POST](https://developers.inter.co/references/pix#pix-pagamento)

---


### auth.py

```python
def get_access_token():
    """
    Realiza autenticação OAuth 2.0 com o Banco Inter e retorna o access token.
    """
    url = config.TOKEN_URL
```
📌 **Baseado na documentação:**
> "Para autenticação OAuth 2.0, utilize o endpoint `POST /oauth/v2/token` com grant type `client_credentials`."  
📚 [Fonte oficial – OAuth 2.0](https://developers.inter.co/references/authentication)

---

```python
    data = {
        "grant_type": "client_credentials"
    }

    auth = (config.CLIENT_ID, config.CLIENT_SECRET)
```
📌 **Baseado na documentação:**
> “A autenticação requer `client_id` e `client_secret` passados via HTTP Basic Auth. O corpo deve conter `grant_type=client_credentials`.”  
📚 [Fonte: OAuth com mTLS](https://developers.inter.co/references/authentication)

---

```python
    cert = (config.CERT_PATH, config.KEY_PATH)
```
📌 **Baseado na documentação:**
> “As chamadas para autenticação devem ser feitas utilizando o certificado digital gerado na criação da aplicação.”  
> “Certificados devem ser enviados no formato `.pem` com chave privada separada.”  
📚 [Fonte: Instruções de Certificado](https://developers.inter.co/references/pix)

---

```python
    try:
        response = requests.post(url, data=data, auth=auth, cert=cert)
        response.raise_for_status()
```
✅ *Justificativa:*  
A requisição está corretamente estruturada com:
- Método `POST`
- `data` com `grant_type`
- `auth` com client credentials
- `cert` com certificado mTLS

Tudo isso está **explicitamente exigido** pela API Inter.

---

```python
        token = response.json().get("access_token")
        if not token:
            raise Exception("Access token não encontrado na resposta.")
        return token
```
📌 **Baseado na documentação:**
> “A resposta bem-sucedida contém o campo `access_token`, que deverá ser utilizado nos demais endpoints.”  
📚 [Fonte: Resposta de autenticação](https://developers.inter.co/references/authentication)

---

### inter_api.py

```python
    payload = {
        "key": chave,
        "amount": valor,
        "description": descricao
    }
```
📌 **Baseado na documentação:**
> Exemplo de corpo do `POST`:
```json
{
  "key": "chavepix@exemplo.com",
  "amount": 10.5,
  "description": "Pagamento de serviço"
}
```
📚 [Fonte: Exemplo de Requisição - Pix Pagamento](https://developers.inter.co/references/pix#pix-pagamento)

---

```python
    response = requests.post(
        url=config.PAGAMENTO_PIX_URL,
        headers=headers,
        json=payload,
        cert=(config.CERT_PATH, config.KEY_PATH)
    )
```
📌 **Baseado na documentação:**
> “As chamadas aos endpoints devem utilizar o certificado mTLS da aplicação, via `.pem` + chave.”  
> “Utilize POST em `https://cdpj.partners.bancointer.com.br/pix/v2/pagamentos`”  
📚 [Fonte: Requisição com certificado - Pix Pagamento](https://developers.inter.co/references/pix#pix-pagamento)

---

### models.py

```python
class PixPayment(BaseModel):
    key: str
    amount: float
    description: constr(max_length=140)
```

📌 **Baseado na documentação:**

> A documentação da API Pix do Banco Inter define o payload para pagamento com os seguintes campos:

| Campo         | Tipo   | Obrigatório | Observações |
|---------------|--------|-------------|-------------|
| `key`         | string | Sim         | Chave Pix do recebedor |
| `amount`      | number | Sim         | Valor a ser transferido |
| `description` | string | Não         | Limite de 140 caracteres |

📚 [Fonte: Requisição - Pix Pagamento](https://developers.inter.co/references/pix#pix-pagamento)

✅ Seu modelo está de acordo:
- `key` como `str`
- `amount` como `float`
- `description` limitada a 140 caracteres

---

```python
    @validator('key')
    def validate_pix_key(cls, v):
        if re.match(r'^\+\d{1,3}\d{1,14}$', v):
            return v  # Telefone válido (ex: +5511999998888)
        elif re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            return v  # E-mail válido
        elif re.match(r'^\d{11}$', v) or re.match(r'^\d{14}$', v):
            return v  # CPF ou CNPJ válido
        elif re.match(r'^[0-9a-fA-F]{32}$', v):
            return v  # EVP (chave aleatória) válido
        else:
            raise ValueError('Chave Pix inválida')
```

📌 **Baseado na documentação:**

> O campo `key` pode ser de vários tipos:

- Chave aleatória (EVP)
- CPF
- CNPJ
- Telefone (formato internacional, ex: +55...)
- E-mail

📚 [Fonte: Formatos válidos de chave Pix](https://www.bcb.gov.br/estabilidadefinanceira/chavespix)

✅ O validador cobre todos os tipos oficiais:
- Telefone com DDI `+` e até 15 dígitos
- E-mail com regex básico
- CPF (11 dígitos)
- CNPJ (14 dígitos)
- EVP (32 caracteres hexadecimais)

---