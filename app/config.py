# app/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega o .env da raiz do projeto
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

# Informações de autenticação
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Certificados
CERT_PATH = os.getenv("CERT_PATH")  # caminho do .pem
KEY_PATH = os.getenv("KEY_PATH")    # caminho da chave privada .pem

# URLs da API do Banco Inter
TOKEN_URL = os.getenv("TOKEN_URL", "https://cdpj.partners.bancointer.com.br/oauth/v2/token")
PAGAMENTO_PIX_URL = os.getenv("PAGAMENTO_PIX_URL", "https://cdpj.partners.bancointer.com.br/banking/v2/pix")

# Modo de teste (ignora chamadas reais à API)
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
