import requests
from app import config

def get_access_token():
    """
    Realiza autenticação OAuth 2.0 com o Banco Inter e retorna o access token.
    Em modo de teste, retorna um token simulado e não faz requisição real.
    """
    if config.TEST_MODE:
        print("TEST_MODE: Simulando autenticação com o Banco Inter...")
        return "fake-access-token"

    url = config.TOKEN_URL
    data = {
        "grant_type": "client_credentials"
    }
    auth = (config.CLIENT_ID, config.CLIENT_SECRET)
    cert = (config.CERT_PATH, config.KEY_PATH)

    try:
        response = requests.post(url, data=data, auth=auth, cert=cert)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            raise Exception("Access token não encontrado na resposta.")
        return token

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro na autenticação com o Banco Inter: {e}")
