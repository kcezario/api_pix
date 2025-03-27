from dataclasses import dataclass
from .pix_gateway_interface import PixGateway

@dataclass
class MockPixGateway(PixGateway):
    def get_config(self) -> dict:
        self.client_id = "fake-client-id"
        self.client_secret = "fake-client-secret"
        self.cert_path = "fake-cert.pem"
        self.key_path = "fake-key.pem"
        self.token_url = "https://mock/token"
        self.payment_url = "https://mock/pix"

    def get_access_token(self) -> str:
        self.get_access_token()
        print("[Mock] Gerando token fake...")
        return "mock-access-token"

    def process_payment(self, key: str, amount: float, description: str) -> dict:
        print("[Mock] Simulando pagamento Pix...")
        print(f"→ key: {key}")
        print(f"→ amount: {amount}")
        print(f"→ description: {description}")
        return {
            "status": "simulado",
            "key": key,
            "amount": amount,
            "description": description,
            "message": "Pagamento simulado com sucesso (modo de teste)"
        }
