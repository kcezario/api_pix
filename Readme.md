### 📜 **Estrutura de Documentação para o Projeto**

---

## **Esqueleto do Projeto - Backend Python para Pagamento Pix com API Banco Inter**

### **Visão Geral**
Este projeto visa implementar a integração com a API do Banco Inter para realizar pagamentos via **Pix**. A API exige um **certificado digital** para autenticação, e durante o desenvolvimento, será utilizado um **Certificado de Teste gerado com OpenSSL**. Para a configuração do ambiente, serão utilizados arquivos `.env` para armazenar as variáveis sensíveis, com diferentes configurações para ambientes de **produção** e **desenvolvimento**.

---

### **1. Certificado de Teste com OpenSSL**

Durante o desenvolvimento, usaremos um certificado **autoassinado** gerado com **OpenSSL** para simular a autenticação com a API do Banco Inter.

#### **Passos para gerar o Certificado de Teste com OpenSSL:**

1. **Gerar a chave privada**:

```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

2. **Gerar o certificado autoassinado (válido por 365 dias)**:

```bash
openssl req -new -x509 -key private_key.pem -out public_cert.pem -days 365
```

3. **Gerar o arquivo `.pfx`** a partir do certificado e chave:

```bash
openssl pkcs12 -export -out certificado.pfx -inkey private_key.pem -in public_cert.pem
```

Este comando irá gerar o arquivo `certificado.pfx`, que será utilizado para autenticação na API do Banco Inter.

> **Nota**: O certificado gerado aqui é autoassinado e serve apenas para testes. Para um ambiente de produção real, você deve adquirir um **certificado digital A1 ou A3** de uma autoridade certificadora.

---

### **2. Configuração do Ambiente de Produção**

O projeto usa um arquivo `.env` para armazenar variáveis sensíveis, como **CLIENT_ID**, **CLIENT_SECRET**, **CAMINHO_DO_CERTIFICADO**, etc. Ele permite que você altere essas variáveis facilmente entre **desenvolvimento** e **produção**.

#### **Estrutura de arquivos:**

```
api_pix/
├── app/
│   ├── __init__.py
│   ├── inter_pix.py
│   └── config.py
├── certs/
│   ├── certificado.pfx
│   └── certificado.pem  # Para uso local com OpenSSL
├── .env
├── .env.prod  # Configuração do ambiente de produção
├── requirements.txt
└── main.py
```

#### **Exemplo de `.env` para Desenvolvimento:**

```env
# .env
CLIENT_ID=seu_client_id
CLIENT_SECRET=seu_client_secret
CERT_PATH=certs/certificado.pem  # Caminho para o certificado gerado com OpenSSL
CERT_PASSWORD=sua_senha_do_certificado
```

#### **Exemplo de `.env.prod` para Produção:**

```env
# .env.prod
CLIENT_ID=seu_client_id_prod
CLIENT_SECRET=seu_client_secret_prod
CERT_PATH=certs/certificado_prod.pfx  # Caminho para o certificado real de produção
CERT_PASSWORD=sua_senha_do_certificado_prod
```

#### **Carregando o ambiente no código:**

Utilize o `dotenv` para carregar as variáveis do arquivo `.env` conforme o ambiente.

```python
# app/config.py
import os
from dotenv import load_dotenv

# Carregar o ambiente correto: desenvolvimento ou produção
env_file = ".env" if os.getenv("ENV") != "production" else ".env.prod"
load_dotenv(env_file)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CERT_PATH = os.getenv("CERT_PATH")
CERT_PASSWORD = os.getenv("CERT_PASSWORD")
```

Agora, o projeto usará variáveis diferentes dependendo do arquivo `.env` que está carregado. Para rodar o ambiente de produção, defina a variável de ambiente `ENV=production`.

---

### **3. Estrutura de Arquivos do Projeto**

A estrutura de arquivos do projeto será organizada da seguinte forma:

```
api_pix/
├── app/
│   ├── __init__.py
│   ├── inter_pix.py     # Integração com a API do Banco Inter
│   └── config.py        # Configuração de variáveis de ambiente e certificados
├── certs/
│   ├── certificado.pfx  # Certificado gerado para teste
│   └── certificado.pem  # Certificado no formato .pem
├── .env                 # Ambiente de Desenvolvimento
├── .env.prod            # Ambiente de Produção
├── requirements.txt     # Dependências do projeto
└── main.py              # Script principal para execução
```

---

### **4. Como Rodar o Projeto**

#### **Ambiente de Desenvolvimento (Local)**

1. **Instalar as dependências**:

```bash
pip install -r requirements.txt
```

2. **Gerar o certificado de teste com OpenSSL** (caso ainda não tenha feito):

```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl req -new -x509 -key private_key.pem -out public_cert.pem -days 365
openssl pkcs12 -export -out certificado.pfx -inkey private_key.pem -in public_cert.pem
```

3. **Rodar o projeto**:

```bash
python main.py
```

---