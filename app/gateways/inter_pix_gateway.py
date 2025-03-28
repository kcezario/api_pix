import os
import requests
import uuid
from dataclasses import dataclass
from datetime import date
from typing import Optional
from .pix_gateway_interface import PixGateway

@dataclass
class InterPixGateway(PixGateway):
    account_number: Optional[str] = None

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

    def get_access_token(self, scope: str) -> str:
        self.get_config()
        data = {
            "grant_type": "client_credentials",
            "scope": scope
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
        access_token = self.get_access_token("pagamento-pix.write")
        idempotency_key = str(uuid.uuid4())

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "x-id-idempotente": idempotency_key,
        }

        if self.account_number:
            headers["x-conta-corrente"] = self.account_number

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

    def get_payment_status(self, transaction_id: str) -> dict:
        """
        Consulta o status de um pagamento Pix usando o codigoSolicitacao.
        Requer o escopo 'pagamento-pix.read'.
        """
        access_token = self.get_access_token("pagamento-pix.read")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        if self.account_number:
            headers["x-conta-corrente"] = self.account_number

        url = f"{self.payment_url}/{transaction_id}"

        try:
            response = requests.get(
                url=url,
                headers=headers,
                cert=(self.cert_path, self.key_path)
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            print("Erro ao consultar Pix:", e.response.text)
            raise RuntimeError(f"Erro na consulta do Pix: {e}")
