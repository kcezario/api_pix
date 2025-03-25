import requests
from app.config import CLIENT_ID, CLIENT_SECRET, CERT_PATH, CERT_PASSWORD


def get_access_token():
    url = "https://cdpj.partners.bancointer.com.br/oauth/v2/token"
    data = {"grant_type": "client_credentials"}
    auth = (CLIENT_ID, CLIENT_SECRET)
    cert = (CERT_PATH, CERT_PASSWORD)

    # Requisição POST para obter o token
    response = requests.post(url, data=data, auth=auth, cert=cert)

    # Verifica se a requisição foi bem-sucedida
    response.raise_for_status()

    # Retorna o token de acesso
    return response.json()["access_token"]


def efetuar_pagamento_pix(access_token, txid, valor, chave_destino, descricao):
    url = "https://cdpj.partners.bancointer.com.br/pix/v2/pix/payments"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "valor": valor,
        "chave": chave_destino,
        "descricao": descricao,
        "txid": txid,
    }

    cert = (CERT_PATH, CERT_PASSWORD)
    response = requests.post(url, json=payload, headers=headers, cert=cert)
    response.raise_for_status()
    return response.json()

def consultar_pagamento(access_token, txid):
    url = f"https://cdpj.partners.bancointer.com.br/pix/v2/pix/payments/{txid}"
    headers = {"Authorization": f"Bearer {access_token}"}
    cert = (CERT_PATH, CERT_PASSWORD)

    response = requests.get(url, headers=headers, cert=cert)
    response.raise_for_status()
    return response.json()