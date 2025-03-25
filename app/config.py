import os
from dotenv import load_dotenv

# Carregar o ambiente correto (desenvolvimento ou produção)
env_file = ".env" if os.getenv("ENV") != "production" else ".env.prod"
load_dotenv(env_file)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CERT_PATH = os.getenv("CERT_PATH")
CERT_PASSWORD = os.getenv("CERT_PASSWORD")
