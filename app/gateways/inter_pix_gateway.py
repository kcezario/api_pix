import os
import requests
import uuid
from dataclasses import dataclass
from datetime import date
from .pix_gateway_interface import PixGateway

@dataclass
class InterPixGateway(PixGateway):
    def get_config(self) -> dict:
        """
        Carrega as variáveis de ambiente com prefixo INTER_ e retorna um dicionário.
        Também atualiza os atributos da instância.
        """
        self.client_id = os.getenv("INTER_CLIENT_ID")
        self.client_secret = os.getenv("INTER_CLIENT_SECRET")
        self.cert_path = os.getenv("INTER_CERT_PATH")
        self.key_path = os.getenv("INTER_KEY_PATH")
        self.token_url = os.getenv("INTER_TOKEN_URL")
        self.payment_url = os.getenv("INTER_PAGAMENTO_PIX_URL")

    def get_access_token(self) -> str:
        self.get_config()
        data = {
            "grant_type": "client_credentials",
            "scope": "pagamento-pix.write"
        }

        auth = (self.client_id, self.client_secret)
        cert = (self.cert_path, self.key_path)

        response = requests.post(
            url=self.token_url,
            data=data,
            auth=auth,
            cert=cert,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            raise Exception("Access token não encontrado na resposta.")
        return token

    def process_payment(self, key: str, amount: float, description: str) -> dict:
        access_token = self.get_access_token()
        idempotency_key = str(uuid.uuid4())

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "x-id-idempotente": idempotency_key,
            # "x-conta-corrente": "12345678"  # opcional: informar a conta corrente caso haja mais de uma
        }

        payload = {
            "valor": f"{amount:.2f}",
            "descricao": description,
            "destinatario": {
                "tipo": "CHAVE",
                "chave": key
            }
        }
        try:
            response = requests.post(
                url=self.payment_url,
                headers=headers,
                json=payload,
                cert=(self.cert_path, self.key_path)
            )

            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            print("Resposta detalhada:", e.response.text)
            raise RuntimeError(f"Erro ao realizar pagamento Pix: {e}")
