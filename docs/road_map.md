
---

## ✅ **Roteiro Completo: Backend em Python para Pagamentos Pix com Banco Inter**

---

### **🎯 Objetivo**
> Desenvolver um backend em Python que realize **pagamentos via Pix**, utilizando a **API oficial do Banco Inter**, para automatizar transações financeiras da empresa.

---

### **🔧 Pré-requisitos**

1. **Conta PJ no Banco Inter**
2. **Chave Pix ativa**
3. **Certificado Digital (.crt + .key ou .pfx)**
4. **Client ID e Secret do app criado no portal Inter**
5. **Python 3.8+**
6. Bibliotecas:
   - `requests`
   - `cryptography` (para uso com certificados)
   - `python-dotenv` (opcional, para gerenciar variáveis de ambiente)

---

### **📁 Estrutura Sugerida do Projeto**

```
pix_backend/
├── app/
│   ├── __init__.py
│   ├── inter_pix.py  # Integração com API do Inter
│   └── config.py     # Carrega variáveis e certificados
├── certs/
│   ├── certificado.pfx
│   └── certificado.pem (opcional)
├── .env
├── requirements.txt
└── main.py
```

---

### **🔐 Etapa 1: Autenticação com a API do Banco Inter**

A API do Inter usa **OAuth 2.0 com client_credentials** e **certificado digital**.

#### 👉 Passos:
1. Converter seu `.pfx` para `.pem`, se necessário (para usar com `requests`).
2. Fazer o **POST** para `/oauth/v2/token` com o certificado.

#### 📦 Exemplo de autenticação:

```python
# app/inter_pix.py
import requests
from app.config import CLIENT_ID, CLIENT_SECRET, CERT_PATH, CERT_PASSWORD

def get_access_token():
    url = "https://cdpj.partners.bancointer.com.br/oauth/v2/token"
    data = {
        "grant_type": "client_credentials"
    }
    auth = (CLIENT_ID, CLIENT_SECRET)
    cert = (CERT_PATH, CERT_PASSWORD)

    response = requests.post(url, data=data, auth=auth, cert=cert)
    response.raise_for_status()
    return response.json()["access_token"]
```

---

### **💸 Etapa 2: Efetuar Pagamento Pix (Iniciar Pix)**

Use a rota de **`POST /pix/payments`** da API Pix.

#### 📦 Exemplo de pagamento:

```python
def efetuar_pagamento_pix(access_token, txid, valor, chave_destino, descricao):
    url = "https://cdpj.partners.bancointer.com.br/pix/v2/pix/payments"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "valor": valor,
        "chave": chave_destino,
        "descricao": descricao,
        "txid": txid
    }

    cert = (CERT_PATH, CERT_PASSWORD)
    response = requests.post(url, json=payload, headers=headers, cert=cert)
    response.raise_for_status()
    return response.json()
```

---

### **📡 Etapa 3: Consultar Status do Pagamento**

Use a rota `GET /pix/payments/{txid}`.

```python
def consultar_pagamento(access_token, txid):
    url = f"https://cdpj.partners.bancointer.com.br/pix/v2/pix/payments/{txid}"
    headers = {"Authorization": f"Bearer {access_token}"}
    cert = (CERT_PATH, CERT_PASSWORD)

    response = requests.get(url, headers=headers, cert=cert)
    response.raise_for_status()
    return response.json()
```

---

### **📂 Etapa 4: Configuração via `.env`**

Crie um arquivo `.env`:

```env
CLIENT_ID=seu_client_id
CLIENT_SECRET=seu_client_secret
CERT_PATH=certs/certificado.pfx
CERT_PASSWORD=sua_senha_do_certificado
```

---

### **⚙️ app/config.py**

```python
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CERT_PATH = os.getenv("CERT_PATH")
CERT_PASSWORD = os.getenv("CERT_PASSWORD")
```

---

### **🚀 main.py (Exemplo de uso)**

```python
from app.inter_pix import get_access_token, efetuar_pagamento_pix, consultar_pagamento
import uuid

if __name__ == "__main__":
    token = get_access_token()

    txid = str(uuid.uuid4())[:35]
    pagamento = efetuar_pagamento_pix(
        access_token=token,
        txid=txid,
        valor="10.00",
        chave_destino="chave@pix.com.br",
        descricao="Pagamento automático"
    )

    print("Pagamento iniciado:", pagamento)

    status = consultar_pagamento(token, txid)
    print("Status:", status)
```

---

### **📜 requirements.txt**

```
requests
python-dotenv
cryptography
```

---

### ✅ **Extras e Cuidados**

- Crie uma interface web ou API REST com **FastAPI** ou **Flask** se quiser expor isso.
- Valide e registre todos os erros com logs.
- Proteja seu certificado e `.env` com cuidado!
- Pode usar **txid** como identificador da transação com sua base.

---