import requests
from app import config
from app.auth import get_access_token


def process_pix_payment(key: str, amount: float, description: str) -> dict:
    """
    Realiza um pagamento via Pix usando a API do Banco Inter.
    
    Em modo de teste, simula a requisição sem enviá-la de verdade.

    Parâmetros:
    - key: chave Pix do destinatário
    - amount: valor em reais (float)
    - description: descrição do pagamento
    
    Retorna:
    - dict com os dados da resposta da API ou simulação
    """
    if config.TEST_MODE:
        print("TEST_MODE: Simulando pagamento Pix...")
        print(f"→ key: {key}")
        print(f"→ valor: {amount}")
        print(f"→ description: {description}")
        return {
            "status": "simulado",
            "key": key,
            "amount": amount,
            "description": description,
            "message": "Pagamento simulado com sucesso (modo de teste)"
        }

    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "key": key,
        "amount": amount,
        "description": description
    }

    try:
        response = requests.post(
            url=config.PAGAMENTO_PIX_URL,
            headers=headers,
            json=payload,
            cert=(config.CERT_PATH, config.KEY_PATH)
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro ao realizar pagamento Pix: {e}")
